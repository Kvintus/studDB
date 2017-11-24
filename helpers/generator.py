from bs4 import BeautifulSoup
import random
import requests


class Generator():
    def __init__(self):
        self.mesta = ['Zvolen', 'Krupina', 'Banská Bystrica', 'Detva']

        self.ulice = ['1. mája', '11. marca', '29. augusta', '9. mája', 'A. Hlinku', 'A. Nográdyho', 'A. Bernoláka', 'A. Sládkoviča', 'Bakova Jama', 'Balkán', 'Bariny', 'Belu IV.', 'Borovianska cesta', 'B. Němcovej', 'Bratov Veselovcov', 'Brezová ulica', 'Buková', 'Buzulucká', 'Bystrický rad', 'Centrum', 'Cesta ku Continentalu', 'Cesta na Kráľovej', 'D. Ertla', 'Divadelná', 'Dobronivská cesta', 'Dolná kolónia', 'Družstevná', 'Dubová ulica', 'Dukelských hrdinov', 'E. M. Šoltésovej', 'E. P. Voljanského', 'Elektrárenská', 'F. Hečku', 'Fialková', 'Gaštanová ulica', 'Gen. Asmolova', 'Gen. Svobodu', 'Hať Podharajch', 'Horná kolónia', 'Hrnčiarska', 'Hronská', 'I. Lihoveckého', 'Imatra', 'I. Krasku', 'Jabloňová', 'J. A. Komenského', 'J. Alexyho', 'Jaselská', 'Jaseňová', 'Javorová', 'Jazmínová', 'J. Bánika', 'J. Bottu', 'J. C. Hronského', 'J. D. Matejovie', 'J. Donča', 'Jedľová', 'J. Fándlyho', 'J. Francisciho', 'J. G. Tajovského', 'J. Gagarina', 'J. Hollého', 'J. Jánošíka', 'J. Jesenského', 'J. Jiskru', 'J. Kalinčiaka', 'J. Kollára', 'J. Kozačeka', 'J. Kráľa', 'J. M. Hurbana', 'J. Matušku', 'J. Poničana', 'J. Šafárika', 'J. Švermu', 'Kimovská', 'Kremnická', 'Krupinská cesta', 'K. Šmidkeho', 'Kuzmányho nábrežie', 'Lesnícka', 'Lieskovská cesta', 'Lipová', 'L. Novomeského', 'Ľ. Fullu', 'Ľ. Kubániho', 'Ľ. Medveckého', 'Ľ. Podjavorinskej', 'Ľ. Štúra', 'Marš. Malinovského', 'M. Bazovského', 'M. Bela', 'Medz. dňa detí', 'M. M. Hodžu', 'M. Kukučína', 'Mládežnícka', 'M. Nešpora', 'Mojmírova', 'Môťovská', 'Môťovská cesta', 'Mraziarenská cesta', 'M. Rázusa', 'M. R. Štefánika', 'M.Ferjenčíka', 'Na Hôrke', 'Na Hrádok', 'Na Rovni', 'Na Štepnici', 'Nádvorná', 'Neresnická cesta', 'Nerudova', 'Nevädzová', 'Nezábudkova', 'Nižovec', 'Novozámocká', 'Obrancov mieru', 'Okružná', 'Orgovánova', 'Osada Sekier', 'Partizánska', 'P. Jilemnického', 'Pod dráhami', 'Pod holým brehom', 'Podbeľová', 'P. O. Hviezdoslava', 'Povstaleckých letcov', 'Prachatická', 'Pražská', 'Predmestie', 'Pribinova', 'Pustý hrad', 'Rákoš', 'R. Čelku', 'R. Jašíka', 'Ružová', 'S. Chalupku', 'Slatinské nábrežie', 'Slnečná', 'Smreková', 'Snežienková', 'Sokolská', 'Somolická', 'Sosnová', 'S. Tomášika', 'Strakonická', 'Stráž', 'Strážska cesta', 'Svätoplukova', 'Školská', 'Š. Moyzesa', 'Študentská cesta', 'Š. Višňovského', 'Tehelná', 'T. G. Masaryka', 'Topoľová', 'Trhová', 'Tulská', 'T. Vansovej', 'Unionka', 'Uramova', 'V. P. Tótha', 'Záhonok', 'Železničná']

        self.zenskeMena = ['Alexandra', 'Andrea', 'Kristína', 'Ema', 'Romana', 'Jarmila', 'Júlia', 'Paulína', 'Anna', 'Dominika', 'Zuzana', 'Marcela', 'Nikola', 'Rebeka', 'Martina', 'Mária', 'Michaela', 'Viera', 'Simona']
        self.muzskeMena = ['Adam', 'Rastislav', 'Emil', 'Roman', 'Matej', 'Viktor', 'Alexander', 'Tomáš', 'Jozef', 'Adrián', 'Marián', 'Miroslav', 'Richard', 'Marek', 'Viliam', 'Róbert', 'Peter', 'Pavol']

    def generateStreet(self):
        return str(random.choice(self.ulice)) + ' ' + str(random.randint(0, 25)) + ' ' + str(random.choice(self.mesta))

    def generateMuz(self):
        return str(random.choice(self.muzskeMena))

    def generateZena(self):
        return str(random.choice(self.zenskeMena))

    def generatePhoneNumber(self):
        return '+421 ' + str(random.randint(100, 999)) + ' ' + str(random.randint(100, 999)) + ' ' + str(random.randint(100, 999))

    def generateDateOfBirth(self, start):
        return "{}.{}.{}".format(random.randint(1, 31), random.randint(1, 12), random.randint(start - 16, start - 15))
