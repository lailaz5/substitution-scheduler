from scraping import fetch_timetable, fetch_teachers, fetch_classes, fetch_teacher_classes, fetch_subjects
from flask import Flask, Response, jsonify, request
from logic import analyze_timetable_cell
from sheets import get_dashboard
from urllib.parse import unquote
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    absent_teacher = data.get("absent_teacher")
    day = data.get("day")
    timeslot = data.get("timeslot")

    timetable_data = fetch_timetable(absent_teacher)

    cell_data = timetable_data.get(day, {}).get(timeslot)

    if not cell_data:
        return jsonify({"error": "No timetable entry found"}), 404

    results = analyze_timetable_cell(cell_data, absent_teacher, day, timeslot)
    return jsonify(results)


@app.route('/teachers', methods=['GET'])
def teachers_list():
    teachers_dict = fetch_teachers()
    teachers_list = list(teachers_dict.keys())
    return jsonify(teachers_list), 200


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


@app.route('/<path:teacher_name>_subjects', methods=['GET'])
def subjects(teacher_name):
    decoded_teacher_name = unquote(teacher_name)
    try:
        subjects = fetch_subjects(decoded_teacher_name)
        response_JSON = json.dumps(subjects, ensure_ascii=False, indent=2)
        response = Response(response_JSON, content_type='application/json; charset=utf-8')
        
        return response, 200
    except KeyError:
        return jsonify({'error': 'No results found.'}), 404


@app.route('/<path:teacher_name>_classes', methods=['GET'])
def teacher_classes(teacher_name):
    decoded_teacher_name = unquote(teacher_name)
    try:
        classes = fetch_teacher_classes(decoded_teacher_name)
        response_JSON = json.dumps(classes, ensure_ascii=False, indent=2)
        response = Response(response_JSON, content_type='application/json; charset=utf-8')
        
        return response, 200
    except KeyError:
        return jsonify({'error': 'No results found.'}), 404


@app.route('/classes', methods=['GET'])
def classes_list():
    classes_dict = fetch_classes()
    classes_list = list(classes_dict.keys())
    return jsonify(classes_list), 200


@app.route('/dashboard', methods=['GET'])
def dashboard_sheet():
    dashboard_data = get_dashboard()
    return jsonify(dashboard_data), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')