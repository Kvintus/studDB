from bs4 import BeautifulSoup 
import requests

html_page = requests.get('https://www.gymzv.sk/sk/obsah/ucitelia_zoznam')
soup = BeautifulSoup(html_page.content, 'html.parser')

middle_container = soup.find('div', {'class':'middle'})
print(middle_container.prettify())