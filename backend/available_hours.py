import requests
import json
import os

api_url = 'http://localhost:5000'

def fetch_teachers_list():
    response = requests.get(f'{api_url}/teachers')
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch teachers list. Status code: {response.status_code}')
        return []

def fetch_available_hours(teacher_name):
    response = requests.get(f'{api_url}/{teacher_name}')
    if response.status_code == 200:
        timetable_data = response.json()
        available_hours = []

        for day, hours in timetable_data.items():
            for hour, lesson in hours.items():
                if lesson and 'attivita' in lesson and (lesson['attivita'] == 'Disposiz.' or lesson['attivita'] == 'Progetti/Dispos.'):
                    available_hours.append(f'{day} {hour}')

        return available_hours
    else:
        print(f'Failed to fetch timetable for {teacher_name}. Status code: {response.status_code}')
        return []

def create_available_hours_json():
    teachers_list = fetch_teachers_list()
    available_hours_data = {}

    for teacher_name in teachers_list:
        available_hours = fetch_available_hours(teacher_name)
        teacher_hours = {}

        for hour in available_hours:
            day, time = hour.split()  
            if day in teacher_hours:
                teacher_hours[day].append(time)
            else:
                teacher_hours[day] = [time]

        available_hours_data[teacher_name] = teacher_hours

    json_file_path = 'available_hours.json'
    backend_directory = os.path.dirname(os.path.abspath(__file__))
    full_json_file_path = os.path.join(backend_directory, json_file_path)

    with open(full_json_file_path, 'w') as json_file:
        json.dump(available_hours_data, json_file, indent=4)

    print(f'Available hours data saved to {full_json_file_path}')

if __name__ == '__main__':
    create_available_hours_json()