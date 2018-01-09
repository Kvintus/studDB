from generator import Generator
from bs4 import BeautifulSoup
import sys
import os, inspect
import requests

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from core.sqlClasses import *

gen = Generator()

html_page = requests.get('https://www.gymzv.sk/sk/obsah/ucitelia_zoznam')
soup = BeautifulSoup(html_page.content, 'lxml')

ucitalia = soup.table.findAll('tr')
ucitalia.pop(0)
for ucitel in ucitalia:
    
    #Ziskavanie skut. informacii
    zaznamy = ucitel.findAll('td')
    nameAndOthers = zaznamy[0].text.strip().split()
    
    prof_title = None
    prof_name = ""
    prof_surname = ""

    if len(nameAndOthers) > 2:
        prof_title = nameAndOthers[0].strip()
        prof_name = nameAndOthers[2].strip()
        prof_surname = nameAndOthers[1].strip()
    else:
        prof_name = nameAndOthers[1].strip()
        prof_surname = nameAndOthers[0].strip()

    prof_loc = zaznamy[2].text.strip()
    prof_email = zaznamy[4].a.text.strip()

    #Pridavanie do databazy
    ucitel = Professor(
        profName = prof_name,
        profSurname = prof_surname,
        profLoc = prof_loc,
        profEmail = prof_email,
        profPhone = gen.generatePhoneNumber(),
        profAdress = gen.generateStreet()
    )

    if prof_title:
        ucitel.profTitle = prof_title
    
    db.session.add(ucitel)

db.session.commit()



    
    