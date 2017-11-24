from bs4 import BeautifulSoup
import random
import requests

def getUlice():
    html_page = requests.get('https://sk.wikipedia.org/wiki/Zoznam_ul%C3%ADc_a_n%C3%A1mest%C3%AD_vo_Zvolene')
    soup = BeautifulSoup(html_page.content, 'lxml')

    main_table = soup.find('table', {'class': 'wikitable'})
    rows = main_table.find_all('tr')
    rows.pop(0)
    ulice = []
    for row in rows:
        ulice.append(row.td.a.text)
    
    return ulice

print(getUlice())