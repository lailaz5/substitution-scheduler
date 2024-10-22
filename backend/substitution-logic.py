import mysql.connector as c


API_URL = "http://localhost:5000"


def connect_to_db():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'school_data',
        'raise_on_warnings': True
    }
    return c.connect(**config)


def find_teacher_area_and_subject(teacher, cursor):
    cursor.execute('''
        SELECT a.nome AS area_name, m.nome AS subject_name
        FROM insegnamenti_materie im
        JOIN docenti d ON im.id_docente = d.id
        JOIN materie m ON im.id_materia = m.id
        JOIN aree a ON m.area = a.id
        WHERE d.nome = %s
    ''', (teacher,))
    
    result = cursor.fetchall()

    if result:
        subjects_by_area = {}
        for area_name, subject_name in result:
            if area_name not in subjects_by_area:
                subjects_by_area[area_name] = []
            subjects_by_area[area_name].append(subject_name)

        return subjects_by_area  
    else:
        return {} 


def valid_co_presence(data): 
    return any(".A.E" not in teacher for teacher in data["insegnanti"])


def co_presence(data, absent_teacher, cursor):
    results = {}

    for teacher in data["insegnanti"]:
        if ".A.E" in teacher:  
            continue  

        if teacher not in results:
            results[teacher] = 0

        if "." in teacher and ".A.E" not in teacher:
            results[teacher] += 2  
            continue

        if data["classe"][0] in ['3', '4', '5']:
            substitute_teacher_teaching = find_teacher_area_and_subject(absent_teacher, cursor)
            teacher_teaching = find_teacher_area_and_subject(teacher, cursor)
            
            lab_subject = "Lab. " + data["materia"]
            if data["materia"] or lab_subject in teacher_teaching:
                results[teacher] += 15
            elif any(subject in teacher_teaching for subject in substitute_teacher_teaching):
                results[teacher] += 10

    return results


def find_substitutes(data, absent_teacher, cursor):
    substitute_teacher_teaching = find_teacher_area_and_subject(absent_teacher, cursor)

    cursor.execute('SELECT nome FROM docenti')
    all_teachers = cursor.fetchall()

    substitute_teachers = {}

    for teacher in all_teachers:
        teacher_name = teacher[0]

        if teacher_name == absent_teacher or ".A.E" in teacher_name:
            continue

        teacher_teaching = find_teacher_area_and_subject(teacher_name, cursor)

        substitute_teachers[teacher_name] = 0
        lab_subject = "Lab. " + data["materia"]

        if any(data["materia"] in subjects for subjects in teacher_teaching.values()) or \
           any(lab_subject in subjects for subjects in teacher_teaching.values()):
            substitute_teachers[teacher_name] += 15  
        elif any(area in teacher_teaching for area in substitute_teacher_teaching):
            substitute_teachers[teacher_name] += 5  

    return {k: v for k, v in sorted(substitute_teachers.items(), key=lambda item: item[1], reverse=True) if v > 0}


def analyze_timetable_cell(data, absent_teacher):
    connection = connect_to_db()
    cursor = connection.cursor()

    if data.get("insegnanti") and valid_co_presence(data):
        results = co_presence(data, absent_teacher, cursor)
    else:
        results = find_substitutes(data, absent_teacher, cursor)

    cursor.close()
    connection.close()
    
    return results


if __name__ == '__main__':
    print(analyze_timetable_cell({
      "classe": "3HT-i",
      "materia": "Sistemi e Reti",
      "insegnanti": [
        ".A.E Falda Enrico"
      ],
      "aula": "Aula 92"
    }, "Benatti Lorenzo"))