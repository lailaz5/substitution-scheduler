
    # WIP

from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.isarchimede.edu.it/Orario/index.html').text
main_table = BeautifulSoup(html_text, 'lxml').find('table')

teachers_dict = {}

for row in main_table.find_all('tr'):
    for cell in row.find_all('td'):
        if 'DOCENTI' in cell.text.strip():
            links = cell.find_all('a')
            for link in links:
                teacher_name = link.text.strip()
                teacher_link = link['href']
                teachers_dict[teacher_name] = teacher_link

teacher_html = requests.get(f'https://www.isarchimede.edu.it/Orario/{teachers_dict["Piccolo Gianluca"]}').text
teacher_table = BeautifulSoup(teacher_html, 'lxml').find('table')

timetable = []

for row in teacher_table.find_all('tr'):
    for cell in row.find_all('td'):
        timetable.append(cell.text.strip())
    
#print(timetable)