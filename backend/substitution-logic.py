import requests

API_URL = "http://localhost:5000"

# api endpoint /supplenze_in_corso -> "docente" "classe" "orainizio" "orafine", ...

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


def subject():
    ...


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
        else:
            results[teacher] = 5  

    return results


def find_substitute_teachers(cell, absent_teacher):
    suitable_teachers = {} # name : points

    teacher_list = requests.get(f"{API_URL}/teachers").json()

    for teacher in teacher_list:
        """teacher_classes = requests.get(f"{API_URL}/{teacher}_classes").json() 

        classes = [cell["classe"] for class_name in teacher_classes if class_name[0] in ['3', '4', '5']]"""
        

    return suitable_teachers


def analyze_timetable_cell(cell, absent_teacher):
    results = {}

    if cell["insegnanti"]:  
        results = co_presence(cell, absent_teacher)  
    else:  
        results = find_substitute_teachers(cell, absent_teacher) 

    return results


if __name__ == '__main__':

    print(analyze_timetable_cell({
        "classe": "2MT-i",
        "materia": "STA",
        "insegnanti": [
            ".Esposito Salvatore"
        ],
        "aula": "Lab. Cad-Cam Aula 41"
        }, "Benatti Lorenzo"))