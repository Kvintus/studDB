from generator import Generator
from bs4 import BeautifulSoup
import sys
import os
import requests
import random

#Kvoli tomu ze je o folder vyssie
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlClasses import *

gen = Generator()

def getClassLinks():
    html_page = requests.get('https://www.gymzv.sk/osoby/studenti')
    soup = BeautifulSoup(html_page.content, 'lxml')
    main = soup.find('div', {'class':'middle'})
    linky = []
    for link in main.find_all('a', href=True):
        linky.append('https://www.gymzv.sk' + str(link['href']))
    
    return linky

def main():
    for link in getClassLinks():
        html_page = requests.get(link)
        soup = BeautifulSoup(html_page.content, 'lxml')
        class_name = soup.find('div', {'class':'middle'}).h1.text.strip().split()[1]
        ucitel = soup.find('ol', {'class':'special'}).li.text.strip().split()

        #vytvorenie triedy
        triedny = Professor.query.filter_by(and_(profName = ucitel[0], profSurname = ucitel[1])).first()
        vyber = ['L', 'P']
        trieda = Class(
            className = class_name
            classRoom = str(random.choice(vyber)) + str(random.randint(1,130))
        )

if __name__ == '__main__':
    main()