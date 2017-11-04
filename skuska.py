import urllib.request
import bs4

url = "https://www.gymzv.sk/sk/obsah/ucitelia_zoznam"
req = urllib.request.urlopen(url)
raw = req.read()
soup = bs4.BeautifulSoup(raw, 'html.parser')

print(soup.table.findAll('tr'))