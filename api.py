from flask import Flask, request
from data.Student import Student
from data.DataLayer import DataLayer
from data.Skill import Skill
from data.Professor import Professor
import json

app = Flask(__name__)


# get list of all students
@app.route('/students')
def get_all_students():
    return DataLayer.get_students_as_json()

# get student by email - email will be a path param
@app.route('/students/<email>')
def get_students_by_email(email):
    return DataLayer.get_student_by_email(email)


# get added students per day of the year - day will be a query param
@app.route('/students')
def get_students_added_on_date():
    creation_year = request.args.get('year')
    creation_month = request.args.get('month')
    creation_day = request.args.get('day')
    return


# get count of desired skills (how many of the students desire a specific skill)
@app.route('/skills')
def get_desirable_skill():
    skill = request.args.get('skill')
    return


# get count for how many students have each type of skill
@app.route('/skills')
def get_existing_skills():
    num_of_students = request.args.get('students')
    return


# add a new student (request which will be invoked by admin) - the route will receive a json with the student fields.
@app.route('/students', methods=['POST'])
def add_new_student():
    content = request.json
    student = Student.from_json(content['id_num'], content['first_name'], content['last_name'], content['email'], content['password'])
    DataLayer.add_student(student)
    response = app.response_class(
        response={json.dumps(student.__dict__)},
        status=200,
        mimetype='application/json'
    )
    return response


# login a student(email + password) - the route will receive a json with the data.
@app.route('/login', methods=['POST'])
def login_student():
    return


# edit student - the route will receive a json with the student fields.
@app.route('/students', methods=['PUT'])
def edit_student():
    return


# delete a student
@app.route('/students', methods=['DELETE'])
def delete_student():
    return


if __name__ == '__main__':
    app.run()
