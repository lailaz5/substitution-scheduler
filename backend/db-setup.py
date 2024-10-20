import mysql.connector as c
import requests
import json
import os

API_URL = "http://localhost:5000"

def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docenti (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classi (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sezione TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aree (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materie (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome TEXT NOT NULL,
            area INT,
            FOREIGN KEY(area) REFERENCES aree(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insegnamenti_materie (
            id_docente INT,
            id_materia INT,
            PRIMARY KEY (id_docente, id_materia),
            FOREIGN KEY (id_docente) REFERENCES docenti(id),
            FOREIGN KEY (id_materia) REFERENCES materie(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insegnamenti_classi (
            id_docente INT,
            id_classe INT,
            PRIMARY KEY (id_docente, id_classe),
            FOREIGN KEY (id_docente) REFERENCES docenti(id),
            FOREIGN KEY (id_classe) REFERENCES classi(id)
        )
    ''')


def populate_database(cursor):
    current_directory = os.path.dirname(__file__)
    json_file_path = os.path.join(current_directory, 'subjects.json')

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            subjects_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{json_file_path}' not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return

    for area_name, subjects in subjects_data.items():
        cursor.execute('''
            INSERT INTO aree (nome)
            VALUES (%s)
        ''', (area_name,))
        
        area_id = cursor.lastrowid

        for subject in subjects:
            cursor.execute('''
                INSERT INTO materie (nome, area)
                VALUES (%s, %s)
            ''', (subject, area_id))

    classes = requests.get(f"{API_URL}/classes").json()
    for class_ in classes:
        cursor.execute('''
            INSERT INTO classi (sezione)
            VALUES (%s)
        ''', (class_,))

    teachers = requests.get(f"{API_URL}/teachers").json()
    for teacher in teachers:
        cursor.execute('''
            INSERT INTO docenti (nome)
            VALUES (%s)
        ''', (teacher,))

        teacher_classes = requests.get(f"{API_URL}/{teacher}_classes").json()
        for class_ in teacher_classes:
            cursor.execute('''
                INSERT INTO insegnamenti_classi (id_docente, id_classe)
                SELECT d.id, c.id
                FROM docenti d, classi c
                WHERE d.nome = %s AND c.sezione = %s
            ''', (teacher, class_))

        if "." in teacher:  
            continue

        teacher_subjects = requests.get(f"{API_URL}/{teacher}_subjects").json()
        for subject in teacher_subjects:
            cursor.execute('''
                INSERT INTO insegnamenti_materie (id_docente, id_materia)
                SELECT d.id, m.id
                FROM docenti d, materie m
                WHERE d.nome = %s AND m.nome = %s
            ''', (teacher, subject))


def setup_database():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'raise_on_warnings': True
    }
    
    connection = c.connect(**config)
    cursor = connection.cursor()

    cursor.execute("SHOW DATABASES LIKE 'school_data'")
    database_exists = cursor.fetchone()

    if not database_exists:
        cursor.execute("CREATE DATABASE school_data")
        cursor.execute("USE school_data")
        create_tables(cursor)
        populate_database(cursor)
        connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    setup_database()