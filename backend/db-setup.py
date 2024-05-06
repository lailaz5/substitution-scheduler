import mysql.connector as c
import requests
import json
import os


def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS indirizzi (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descrizione VARCHAR(255) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classi (
            classe VARCHAR(10) PRIMARY KEY,
            indirizzo INT,
            diurno BOOLEAN,
            FOREIGN KEY (indirizzo) REFERENCES indirizzi(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materie (
            id INT AUTO_INCREMENT PRIMARY KEY,
            materia VARCHAR(255) NOT NULL,
            indirizzo_id INT,
            FOREIGN KEY (indirizzo_id) REFERENCES indirizzi(id)
        )
    ''')


def initialize(cursor):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'subjects.json')

    with open(file_path, 'r') as f:
        subjects_mapping = json.load(f)
        for indirizzo, materie_list in subjects_mapping.items():
            cursor.execute("INSERT INTO indirizzi (descrizione) VALUES (%s)", (indirizzo,))
            indirizzo_id = cursor.lastrowid
            for materia in materie_list:
                try:
                    cursor.execute("INSERT INTO materie (materia, indirizzo_id) VALUES (%s, %s)", (materia, indirizzo_id))
                except Exception as e:
                    continue

    classes = requests.get(f'http://localhost:5000/classes').json()

    for class_name in classes:
        indirizzo = None
        diurno = False

        indirizzi_mapping = {
            'I': 'informatica',
            'M': 'meccanica',
            'F': 'meccanica',
            'i': 'informatica',
            'c': 'chimica',
            'a': 'automazione',
            'm': 'meccanica'
        }

        if class_name.endswith('S'):
            if class_name.startswith(('1', '2')):
                indirizzo = 'N/A'
            elif class_name.startswith(('3', '4', '5')):
                for char in class_name:
                    if char in indirizzi_mapping:
                        indirizzo = indirizzi_mapping[char]
                        break
        else:
            diurno = True
            if class_name.startswith(('1', '2')):
                indirizzo = 'N/A'
            elif class_name.startswith(('3', '4', '5')):
                indirizzo = indirizzi_mapping.get(class_name[-1], 'N/A')

        if indirizzo:
            cursor.execute("SELECT id FROM indirizzi WHERE descrizione = %s", (indirizzo,))
            result = cursor.fetchone()
            if result:
                indirizzo_id = result[0]
                cursor.execute("INSERT INTO classi (classe, indirizzo, diurno) VALUES (%s, %s, %s)", (class_name, indirizzo_id, diurno))


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
        initialize(cursor)
        connection.commit()

    cursor.close()
    connection.close()


if __name__ == '__main__':
    setup_database()