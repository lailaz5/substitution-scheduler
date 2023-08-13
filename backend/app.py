from flask import Flask, Response, jsonify
from timetable_scraper import get_timetable, fetch_teachers_dict
from urllib.parse import unquote
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/<path:teacher_name>', methods=['GET'])
def get_teacher_timetable(teacher_name):
    decoded_teacher_name = unquote(teacher_name)  
    try:
        timetable = get_timetable(decoded_teacher_name)
        response_JSON = json.dumps(timetable, ensure_ascii=False, indent=2)
        response = Response(response_JSON, content_type='application/json; charset=utf-8')
        
        return response, 200
    except KeyError:
        return jsonify({'error': 'Teacher not found'}), 404

@app.route('/teachers', methods=['GET'])
def get_list():
    teachers_dict = fetch_teachers_dict()
    teachers_list = list(teachers_dict.keys())
    return jsonify(teachers_list), 200

if __name__ == '__main__':
    app.run(debug=True)