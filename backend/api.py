from flask import Flask, Response, jsonify
from scraping import fetch_timetable, fetch_teachers, fetch_classes
from urllib.parse import unquote
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)


@app.route('/teachers', methods=['GET'])
def teachers_list():
    teachers_dict = fetch_teachers()
    teachers_list = list(teachers_dict.keys())
    return jsonify(teachers_list), 200


@app.route('/<path:teacher_name>_classes', methods=['GET'])
def classes(teacher_name):
    decoded_teacher_name = unquote(teacher_name)  
    try:
        classes = fetch_classes(decoded_teacher_name)
        response_JSON = json.dumps(classes, ensure_ascii=False, indent=2)
        response = Response(response_JSON, content_type='application/json; charset=utf-8')
        
        return response, 200
    except KeyError:
        return jsonify({'error': 'No results found.'}), 404


@app.route('/<path:teacher_name>', methods=['GET'])
def timetable(teacher_name):
    decoded_teacher_name = unquote(teacher_name)  
    try:
        timetable = fetch_timetable(decoded_teacher_name)
        response_JSON = json.dumps(timetable, ensure_ascii=False, indent=2)
        response = Response(response_JSON, content_type='application/json; charset=utf-8')
        
        return response, 200
    except KeyError:
        return jsonify({'error': 'Teacher not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')