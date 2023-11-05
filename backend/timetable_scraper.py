import json
import requests
from bs4 import BeautifulSoup


def fetch_teachers_dict():
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

    return teachers_dict


def extract_data(cell):
    data = [content.text.strip() for content in cell.find_all(text=True) if content.strip() != '']
    
    if not data:
        return None

    if len(data) == 1:
        return {
            'attivita': data[0]
        }

    class_name = data[0]
    classroom = data[-1]
    subject = data[1]

    teachers = []

    if len(data) >= 4:
        teachers = data[2:-1]

    if class_name != '.R.P.':
        if not teachers:
            return {
                'classe': class_name,
                'materia': subject,
                'aula': classroom
            }
        else:
            return {
                'classe': class_name,
                'materia': subject,
                'insegnanti': teachers,
                'aula': classroom
            }
    else:
        return {
            'attivita': class_name,
            'insegnanti': teachers if teachers else None,
            'aula': classroom
        }


def get_timetable(teacher):
    teachers_dict = fetch_teachers_dict()

    teacher_html = requests.get(f'https://www.isarchimede.edu.it/Orario/{teachers_dict[teacher]}').text
    teacher_table = BeautifulSoup(teacher_html, 'lxml').find('table')

    rows = iter(teacher_table.find_all('tr'))
    days = [day.strip() for day in next(rows).text.split() if day.strip()]
    hours = []

    timetable = [[] for _ in days]

    for time_index, row in enumerate(rows):
        columns = iter(row.find_all('td'))
        lesson_time = next(iter(next(columns).find_all('p'))).text.strip()
        hours.append(lesson_time)
        day_index = 0
        for cell in columns:
            while day_index < len(days) and len(timetable[day_index]) > time_index:
                day_index += 1
            lesson_duration = int(cell['rowspan'])
            for _ in range(lesson_duration):
                timetable[day_index].append(extract_data(cell))

    timetable_data = {}

    for day, lessons in zip(days, timetable):
        timetable_data[day] = {}
        for lesson_time, lesson in zip(hours, lessons):
            timetable_data[day][lesson_time] = lesson

    return timetable_data


if __name__ == '__main__':
    example = get_timetable("Piccolo Gianluca")
    print(json.dumps(example, indent=4))