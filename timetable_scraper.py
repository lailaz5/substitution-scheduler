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

                    # Remove asterisk from teacher name if present
                    teacher_name = teacher_name.replace('*', '')

                    teacher_link = link['href']
                    teachers_dict[teacher_name] = teacher_link

    return teachers_dict


def extract_data(cell):
    # Extracts the relevant data from a cell in the timetable
    data = [thing.text.strip() for thing in cell.find_all('p', id='nodecBlack')]

    if not data:
        return None

    if len(data) == 1:
        return {
            'attivita': data[0]
        }

    class_name = data[0]
    classroom = data[-1]
    subject = data[1]

    if len(data) >= 4:
        teachers = data[2]
    else:
        if class_name != 'Ricevimento Parenti':
            return {
                'classe': class_name,
                'materia': subject,
                'aula': classroom
            }
        else:
            return {
                'attivita': class_name,
                'insegnanti': subject,
                'aula': classroom
            }

    return {
        'classe': class_name,
        'materia': subject,
        'insegnanti': teachers,
        'aula': classroom
    }


def get_timetable(teacher):
    # Retrieves the timetable for the given teacher
    teachers_dict = fetch_teachers_dict()

    teacher_html = requests.get(f'https://www.isarchimede.edu.it/Orario/{teachers_dict[teacher]}').text
    teacher_table = BeautifulSoup(teacher_html, 'lxml').find('table')

    rows = iter(teacher_table.find_all('tr'))
    days = [day.strip() for day in next(rows).text.split() if day.strip()]
    hours = []

    timetable = [[] for _ in days]

    for time_idx, row in enumerate(rows):
        columns = iter(row.find_all('td'))
        lesson_time = next(iter(next(columns).find_all('p'))).text.strip()
        hours.append(lesson_time)
        day_idx = 0
        for cell in columns:
            # Update the day index based on the number of lessons already added
            while day_idx < len(days) and len(timetable[day_idx]) > time_idx:
                day_idx += 1
            lesson_duration = int(cell['rowspan'])
            for _ in range(lesson_duration):
                timetable[day_idx].append(extract_data(cell))

    timetable_data = {}

    for day, lessons in zip(days, timetable):
        timetable_data[day] = {}
        for lesson_time, lesson in zip(hours, lessons):
            timetable_data[day][lesson_time] = lesson

    return timetable_data


if __name__ == '__main__':
    # Example usage: retrieve and print the timetable for a specific teacher
    example = get_timetable("Saddemi Gabriella")
    print(json.dumps(example, indent=4))
