from bs4 import BeautifulSoup
import requests
import json


default_url = 'https://www.isarchimede.edu.it/Orariodocenti'


def fetch_teachers():
    html_text = requests.get(f'{default_url}/index.html').text
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


def fetch_classes(teacher):
    classes = []
    teachers_dict = fetch_teachers()
    teacher_html = requests.get(f'{default_url}/{teachers_dict[teacher]}').text
    teacher_table = BeautifulSoup(teacher_html, 'html.parser').find('table')

    if teacher_table:
        for row in teacher_table.find_all('tr')[1:]:
            columns = row.find_all('td')[1:]

            for column in columns:
                class_name_tag = column.find('p')

                if class_name_tag:
                    class_name = class_name_tag.text.strip()  
                    if class_name and class_name not in classes and len(class_name) == 5 and class_name != '.R.P.':
                        classes.append(class_name)

    return classes


def fetch_classes():
    html_text = requests.get(f'{default_url}/index.html').text
    main_table = BeautifulSoup(html_text, 'lxml').find('table')

    classes = {}

    if main_table:
        for row in main_table.find_all('tr'):
            for cell in row.find_all('td'):
                if 'CLASSI' in cell.text.strip():
                    links = cell.find_all('a')
                    for link in links:
                        class_name = link.text.strip()
                        class_link = link['href']
                        classes[class_name] = class_link

    return classes


def fetch_subjects(teacher):
    timetable = fetch_timetable(teacher)
    subjects = []

    for day, lessons in timetable.items():
        for lesson_time, lesson in lessons.items():
            if lesson and 'materia' in lesson:
                subject = lesson['materia']
                if len(subject) != 5 or '-' not in subject:  
                    if not any(char.isdigit() for char in subject):  
                        if subject not in subjects:
                            subjects.append(subject)

    return subjects


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
    subject = data[-2]  

    teachers = []

    if len(data) > 3:  
        teachers = data[1:-2]  

    if subject != '.R.P.':
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
        teachers.append(class_name)
        return {
            'attivita': subject,
            'insegnanti': teachers if teachers else None,
            'aula': classroom
        }


def fetch_timetable(teacher):
    teachers_dict = fetch_teachers()

    teacher_html = requests.get(f'{default_url}/{teachers_dict[teacher]}').text
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
    teacher = "Piccolo Gianluca"
    timetable = fetch_timetable(teacher)
    classes = fetch_classes(teacher)
    print(json.dumps(timetable, indent=4))
    print(json.dumps(classes, indent=4))