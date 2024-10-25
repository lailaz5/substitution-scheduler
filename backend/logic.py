import mysql.connector as c
import requests


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


def day_off(day_timetable):
    return all(period is None for period in day_timetable.values())


def check_teacher_availability(teacher, day, timeslot):
    try:
        teacher_timetable = requests.get(f"{API_URL}/{teacher}").json()
        
        day_timetable = teacher_timetable.get(day, {})
        
        if day_off(day_timetable):
            return False 

        availability = day_timetable.get(timeslot)
        
        if availability is None:
            return True
        
        other_teachers = availability.get("insegnanti", [])
        
        has_valid_teacher = any(".A.E." not in other_teacher for other_teacher in other_teachers)

        return has_valid_teacher

    except Exception as e:
        print(f"Error checking availability for {teacher}: {e}")
        return False


def classes_taught_to(class_, teacher, cursor):
    cursor.execute('''
        SELECT COUNT(*) FROM insegnamenti_classi ic
        JOIN classi c ON ic.id_classe = c.id
        JOIN docenti d ON ic.id_docente = d.id
        WHERE c.sezione = %s AND d.nome = %s
    ''', (class_, teacher))

    result = cursor.fetchone()
    return result[0] > 0  


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


def find_substitutes(data, absent_teacher, day, timeslot, cursor):
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

        if classes_taught_to(data["classe"], teacher_name, cursor):
            substitute_teachers[teacher_name] += 2

    sorted_teachers = {k: v for k, v in sorted(substitute_teachers.items(), key=lambda item: item[1], reverse=True) if v > 0}

    available_teachers = {}
    for teacher_name in sorted_teachers:
        if check_teacher_availability(teacher_name, day, timeslot):
            available_teachers[teacher_name] = sorted_teachers[teacher_name]

    return available_teachers


def analyze_timetable_cell(data, absent_teacher, day, timeslot):
    connection = connect_to_db()
    cursor = connection.cursor()

    if data.get("insegnanti") and valid_co_presence(data):
        results = co_presence(data, absent_teacher, cursor)
    else:
        results = find_substitutes(data, absent_teacher, day, timeslot, cursor)

    cursor.close()
    connection.close()
    
    return results