from flask import Flask, jsonify
from timetable_scraper import get_timetable
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/<path:teacher_name>', methods=['GET'])
def get_teacher_timetable(teacher_name):
    decoded_teacher_name = unquote(teacher_name)  # Decode the URL parameter
    try:
        timetable = get_timetable(decoded_teacher_name)
        return jsonify(timetable), 200
    except KeyError:
        return jsonify({'error': 'Teacher not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)