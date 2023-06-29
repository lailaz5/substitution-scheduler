
    # WIP

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
                teachers_links.append(link['href'])

#teacher = 'Piccolo Gianluca.html' ---> n.112 in the list

teacher_html = requests.get(f'https://www.isarchimede.edu.it/Orario/{teachers_links[112]}').text
teacher_table = BeautifulSoup(teacher_html, 'lxml').find('table')

timetable = []

for row in teacher_table.find_all('tr'):
    timetable.append(row.text.strip())
    '''for cell in row.find_all('td'):
        classes.append(cell.text.strip())'''

print(timetable)