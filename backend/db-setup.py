from selection import determine_sector
import mysql.connector as c
import requests
import json
import os


api_base_url = 'http://localhost:5000'


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
        CREATE TABLE IF NOT EXISTS docenti (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            indirizzo INT,
            punti_disponibilita INT,
            ore_supp_effettuate INT,
            ore_supp_minime INT,
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
        indirizzi_values = [(indirizzo,) for indirizzo in subjects_mapping.keys()]
        cursor.executemany("INSERT INTO indirizzi (descrizione) VALUES (%s)", indirizzi_values)
        
    cursor.execute("SELECT id, descrizione FROM indirizzi")
    indirizzi_ids = {row[1]: row[0] for row in cursor}

    materie_values = [(materia, indirizzi_ids[indirizzo]) for indirizzo, materie_list in subjects_mapping.items() for materia in materie_list]
    cursor.executemany("INSERT INTO materie (materia, indirizzo_id) VALUES (%s, %s)", materie_values)

    teachers_response = requests.get(f'{api_base_url}/teachers').json()
    classes_response = requests.get(f'{api_base_url}/classes').json()
    
    teachers = [(teacher, determine_sector(teacher)) for teacher in teachers_response]
    
    classi_values = []
    
    for class_name in classes_response:
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
            indirizzo_id = indirizzi_ids.get(indirizzo)
            if indirizzo_id is not None:
                classi_values.append((class_name, indirizzo_id, diurno))
            else:
                print(f"Indirizzo '{indirizzo}' not found in indirizzi_ids.")

    cursor.executemany("INSERT INTO classi (classe, indirizzo, diurno) VALUES (%s, %s, %s)", classi_values)

    docenti_values = [(teacher_name, indirizzi_ids.get(area), 0, 0, 0) for teacher_name, area in teachers]
    cursor.executemany("INSERT INTO docenti (nome, indirizzo, punti_disponibilita, ore_supp_effettuate, ore_supp_minime) VALUES (%s, %s, %s, %s, %s)", docenti_values)


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