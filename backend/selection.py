import requests
import json
import os


current_dir = os.path.dirname(__file__)
subjects_file_path = os.path.join(current_dir, 'subjects.json')

with open(subjects_file_path, 'r') as f:
    specializations_mapping = json.load(f)


def determine_sector(teacher):
    if teacher[0] == '.':
        return "N/A"

    subjects_response = requests.get(f'http://localhost:5000/{teacher}_subjects')

    if subjects_response.status_code != 200:
        return "N/A"

    subjects = subjects_response.json()

    teaching_specializations = set()

    for subject in subjects:
        for specialization, predefined_subjects in specializations_mapping.items():
            if subject in predefined_subjects:
                teaching_specializations.add(specialization)
                break

    if teaching_specializations:
        return ', '.join(teaching_specializations)
    else:
        return "N/A"


if __name__ == '__main__':
    teaching_specialization = determine_sector("Piccolo Gianluca")
    print(teaching_specialization)