from bs4 import BeautifulSoup
from urllib.request import urlopen

import pandas as pd
import re

counter=0
all_row_data=[]


for index in range(0,6):
#for index in range(0,1):

    ## loop for each page while changing number on url
    url="https://www.----------------------/pagina"+str(index)


    html = urlopen(url)
    content=html.read()

    soup=BeautifulSoup(content)


    for test in soup.find_all('div',{'class':'media-body'}):
        row_data = []
        print(counter)







        #print(soup_internal)




        ##get names-A
        #print(test.find('h4').text)
        row_data.insert(0,' '.join(test.find('h4').text.split()))
        ##get sublink-
        #print(test.find('p',{'class':'description'}).text)
        ##get sublink-
        #print(test.find('span', {'class': 'title hidden-xs'}).text)
        ##get sublink-B
        #print(test.find('span', {'class': 'context'}).text)
        row_data.insert(1, ''.join(test.find('span', {'class': 'context'}).text.split()))
        ##got links
        # print(test.find('a'))
        ##loop for each list item while getting <a tag>
        ##go to <a> tag and scrape content
        html2 = 'https://www.zorgkaartnederland.nl' + test.find('a').get('href')
        content_insider = urlopen(html2).read()
        soup_internal = BeautifulSoup(content_insider)





        ##get names-C
        # print( soup_internal.find('h1', {'class', 'title'}).text)
        row_data.insert(2, ''.join(soup_internal.find('h1', {'class', 'title'}).text.split()))

        # print(soup_internal.find('p').text)
        row_data.insert(3, ''.join(soup_internal.find('p').text.split()))

        # print(soup_internal.find('span',{'class', 'address_content'}).text)
        row_data.insert(4, ''.join(soup_internal.find('span', {'class', 'address_content'}).text.split()))

        # print(soup_internal.find('div', {'class', 'address_row'}).text)
        row_data.insert(5, ''.join(soup_internal.find('div', {'class', 'address_row'}).text.split()))

        # print(soup_internal.find('span',attrs={"itemprop": "telephone"}).text)

        row_data.insert(6, ''.join(soup_internal.find('span', attrs={"itemprop": "telephone"}).text.split()))

        # print(soup_internal.find('div', {'class', 'col-xs-12 col-sm-6 col-md-7'}).text)

        start = 'Adres'
        end = 'Telefoon'
        s = soup_internal.find('div', {'class', 'col-xs-12 col-sm-6 col-md-7'}).text

        row_data.insert(7, ' '.join(s[s.find(start) + len(start):s.rfind(end)].split()))

        start1 = 'Website'
        end1 = 'Zijn'
        end2='Locatie'
        x=' '.join(s[s.find(start1) + len(start1):s.rfind(end1)].split())

        ss=x[x.find(start1) + len(start1): x.rfind(end2)]
        if ss.strip().endswith('nl'):
            row_data.insert(8, ss[1:])
        else:
            row_data.insert(8, ss[1:] + 'l')

        # print(soup_internal_twice.find('div', {'class', 'text_block'}).text)

        if 'Specialisten' in soup_internal.find('ul', {'class', 'nav nav-tabs'}).text:

            # get specialists
            content_insider_twice = urlopen(html2 + '/specialisten').read()
            soup_internal_twice = BeautifulSoup(content_insider_twice)


            row_data.insert(9, re.findall(r'\d+',''.join(soup_internal_twice.find('div', {'class', 'text_block'}).text.split()))[0])
        else:
            row_data.insert(9, '')

        counter=counter+1
        print(row_data)

        all_row_data.append(row_data)

    ##write content to excel
column_headers=['A','C','3','4','5','6','7','B','E','D']

df = pd.DataFrame(all_row_data, columns=column_headers)

df.to_excel("test_table_a.xlsx")
df.to_csv("test_table_a.csv")
