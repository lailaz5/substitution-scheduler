from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.isarchimede.edu.it/Orario/index.html').text


table = BeautifulSoup(html_text, 'lxml').find('table')

teachers_links = []

for row in table.find_all('tr'):
    for cell in row.find_all('td'):
        if 'DOCENTI' in cell.text.strip():
            links = cell.find_all('a')
            for link in links:
                #print(link.text.strip())
                teachers_links.append(link['href'])

#print(teachers_links)