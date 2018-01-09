from generator import Generator
from bs4 import BeautifulSoup
import sys
import os
import requests
import random

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from core.sqlClasses import *
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
    links = getClassLinks()
    links.pop(len(links)-1)
    links.pop(len(links)-1)
    for link in getClassLinks():
        html_page = requests.get(link)
        soup = BeautifulSoup(html_page.content, 'lxml')
        class_name = soup.find('div', {'class':'middle'}).h1.text.strip().split()[1]
        ucitel = soup.find('ol', {'class':'special'}).li.text.strip().split()

        print(ucitel)

        #vytvorenie triedy
        if len(ucitel) >= 3:
            triedny = Professor.query.filter_by(profSurname= ucitel[1], profName = ucitel[2]).first()
        else:
            triedny = Professor.query.filter_by(profSurname = ucitel[0], profName = ucitel[1]).first()

        print(triedny.profSurname)

        vyber = ['L', 'P']
       
        trieda = Class(
            classLetter = class_name[-1:],
            classRoom = str(random.choice(vyber)) + str(random.randint(1,130)),
            classStart = int(link[-5:-1])
        )
        trieda.profs.append(triedny)
        db.session.add(trieda)

        #generovanie ziakov
        ziaci_mena  = soup.find_all('ol', {'class':'special'})[1].find_all('li')
        ziaciMenaFin = []
        for ziak in ziaci_mena:
            ziaciMenaFin.append(ziak.span.text.split())
        
        
        for ziak in ziaciMenaFin:
            
            novyZiak = Students(
                studentName = ziak[1],
                studentSurname = ziak[0],
                studentDateOfBirth = gen.generateDateOfBirth(trieda.classStart),
                studentStart = trieda.classStart,
                studentAdress = gen.generateStreet(),
                studentEmail = "{}.{}@gymzv.sk".format(ziak[0], ziak[1]),
                studentPhone = gen.generatePhoneNumber()
            )

            novyZiak.classes.append(trieda)
            db.session.add(novyZiak)
        db.session.commit()

if __name__ == '__main__':
    main()