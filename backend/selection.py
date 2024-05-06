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

    teaching_specialization = set()

    for subject in subjects:
        found_specialization = None
        for specialization, predefined_subjects in specializations_mapping.items():
            if subject in predefined_subjects:
                found_specialization = specialization
                break
        if found_specialization is None:
            return "N/A"
        else:
            teaching_specialization.add(found_specialization)

    if len(teaching_specialization) > 1:
        return "N/A"

    if teaching_specialization:
        return teaching_specialization.pop()
    else:
        return "N/A"


if __name__ == '__main__':
    teaching_specialization = determine_sector("Piccolo Gianluca")
    print(teaching_specialization)