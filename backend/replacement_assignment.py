import requests
from timetable_scraper import fetch_teachers_dict

def fetch_API(teacher_name):
    url = f'http://127.0.0.1:5000/{teacher_name}'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return "Response is not valid JSON."
    else:
         return f"Error: {response.status_code} - {response.text}"

def available_hours(teacher_name, target_day):
    timetable = fetch_API(teacher_name)
    hours = []
    
    if target_day in timetable:
        for time, details in timetable[target_day].items():
            if details and "attivita" in details and details["attivita"] == "Disposiz.":
                hours.append(time)
    
    return hours

if __name__ == '__main__':
    teacher_dict = fetch_teachers_dict()
    
    for teacher_name in teacher_dict:
        target_day = "LUN"
        
        disposiz_times = available_hours(teacher_name, target_day)
        
        if disposiz_times:
            print(f"{teacher_name} at hours:", ', '.join(disposiz_times))

    print('DONE')