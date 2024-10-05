import requests
import json
import os

API_URL = "http://localhost:5000"

# /supplenze_in_corso -> "docente" "classe" "orainizio" "orafine", ...

def specialization(teacher, absent_teacher, cell):
    absent_teacher_classes = requests.get(f"{API_URL}/{absent_teacher}_classes").json()  
    teacher_classes = requests.get(f"{API_URL}/{teacher}_classes").json()

    if cell["classe"][0] in ['3', '4', '5']:
        last_letters_absent = [class_name[-1] for class_name in absent_teacher_classes if class_name[0] in ['3', '4', '5']]
        last_letters_teacher = [class_name[-1] for class_name in teacher_classes if class_name[0] in ['3', '4', '5']]

        if last_letters_absent and last_letters_teacher:
            if any(letter in last_letters_absent for letter in last_letters_teacher):
                return True  

    return False


def co_presence(cell, absent_teacher):
    results = {}

    for teacher in cell["insegnanti"]:
        if ".A.E" in teacher:  
            continue  

        if "." in teacher and ".A.E" not in teacher:
            results[teacher] = 2  
            continue

        if specialization(teacher, absent_teacher, cell):
            results[teacher] = 10  

            teacher_classes = requests.get(f"{API_URL}/{teacher}_classes").json()
            if cell["classe"] in teacher_classes:
                results[teacher] += 10  

    return results


def by_subject(teacher):
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, 'subjects.json')

    with open(file_path, 'r') as f:
        subjects_areas = json.load(f)

    try:
        teacher_subjects = requests.get(f"{API_URL}/{teacher}_subjects").json()
    except requests.RequestException as e:
        print(f"Error fetching data for teacher {teacher}: {e}")
        return None

    teacher_subjects = [subject.lower() for subject in teacher_subjects]

    matched_areas = set()

    for area, subjects in subjects_areas.items():
        for subject in subjects:
            subject_lower = subject.lower()

            if any(subject_lower == ts for ts in teacher_subjects):
                matched_areas.add(area)

    if len(matched_areas) == 0:
        return None

    matched_area = list(matched_areas)[0]

    try:
        all_teachers = requests.get(f"{API_URL}/teachers").json()
    except requests.RequestException as e:
        print(f"Error fetching data for teachers list: {e}")
        return None

    teachers_points = {}

    for other_teacher in all_teachers:
        if other_teacher == teacher:
            continue

        if "." in other_teacher:  
            continue  

        try:
            other_teacher_subjects = requests.get(f"{API_URL}/{other_teacher}_subjects").json()
        except requests.RequestException as e:
            print(f"Error fetching data for teacher {other_teacher}: {e}")
            continue 

        other_teacher_subjects = [subject.lower() for subject in other_teacher_subjects]

        for subject in subjects_areas[matched_area]:
            if subject.lower() in other_teacher_subjects:
                teachers_points[other_teacher] = 13
                break  

    return teachers_points


def find_substitute_teachers(cell, absent_teacher):
    suitable_teachers = {} # nome : punti

    suitable_teachers = by_subject(absent_teacher)

    print("DONE")
        
    return suitable_teachers


def analyze_timetable_cell(cell, absent_teacher):
    results = {}

    if cell.get("insegnanti"):
        results = co_presence(cell, absent_teacher)
    else:
        results = find_substitute_teachers(cell, absent_teacher)

    return results


if __name__ == '__main__':

    print(analyze_timetable_cell({
      "classe": "3HT-i",
      "materia": "Sistemi e Reti",
      "aula": "Aula 92"
    }, "Benatti Lorenzo"))