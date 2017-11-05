from bs4 import BeautifulSoup
import sys
import requests
import sqlite3
from cs50 import SQL


html_page = requests.get('https://www.gymzv.sk/sk/obsah/ucitelia_zoznam')
soup = BeautifulSoup(html_page.content, 'lxml')

ucitalia = soup.table.findAll('tr')
ucitalia.pop(0)
for ucitel in ucitalia:
    zaznamy = ucitel.findAll('td')
    print(len(zaznamy))
