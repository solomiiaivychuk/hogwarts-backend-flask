from flask import Flask, request
from data.Student import Student
from data.DataLayer import DataLayer
from data.Skill import Skill
from data.Professor import Professor
import json

app = Flask(__name__)

"""
The function will create a new dataLayer instance to be used by the flask app.
Which will invoke the previously created function in order to populate the
DataLayer’s students dictionary
"""


# get list of all students
@app.route('/students')
def get_all_students():
    return DataLayer.get_students_as_json()


# get student by email - email will be a path param
@app.route('/students/<email>')
def get_students_by_email(email):
    return DataLayer.get_student_by_email(email)


# get added students per day of the year - day will be a query param
@app.route('/students/date')
def get_students_added_on_date():
    creation_year = request.args.get('year')
    creation_month = request.args.get('month')
    creation_day = request.args.get('day')
    for k, v in DataLayer.students.items():
        if creation_year == v._creation_time[:4] and\
                creation_month == v._creation_time[5:7] and \
                creation_day == v._creation_time[8:10]:
            return v.__str__()
        else:
            return str.format("No students were added on {}-{}-{}", creation_year, creation_month, creation_day)


# get count of desired skills (how many of the students desire a specific skill)
@app.route('/skills/wish')
def get_desirable_skill():
    skill = request.args.get('skill')
    return DataLayer.get_desired_skill(skill)



# get count for how many students have each type of skill
@app.route('/skills')
def get_existing_skills():
    skill = request.args.get('skill')
    return DataLayer.get_existing_skill(skill)


# add a new student (request which will be invoked by admin) - the route will receive a json with the student fields.
@app.route('/students', methods=['POST'])
def add_new_student():
    content = request.json
    student = Student.from_json(content['id_num'], content['first_name'], content['last_name'], content['email'],
                                content['password'])
    if student is None:
        return "Please make sure that all fields are filled"
    if student._email in DataLayer.students:
        return "The student with this email already exists"
    else:
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
    content = request.json
    email = content['email']
    password = content['password']
    if email in DataLayer.students:
        if password == DataLayer.students[email].get_password():
            return "Logged in successfully"
        else:
            return "Wrong password"
    else:
        return "The email is not in the students database"


@app.route('/skills', methods=['POST'])
def add_skill_to_student():
    content = request.json
    email = content["email"]
    skill_name = content["skill"]
    skill_level = content["level"]
    skill = Skill(skill_name, skill_level)
    if email in DataLayer.students:
        DataLayer.add_skill(DataLayer.students[email], skill)
        student_name = DataLayer.students[email].get_first_name() + " " + DataLayer.students[email].get_last_name()
        response = app.response_class(
            response={
                str.format("Student {} acquired new skill {} on a level {}", student_name, skill.name, skill.level)},
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "There is no student with this email"


@app.route('/skills/wish', methods=['POST'])
def add_desired_skill_to_student():
    content = request.json
    email = content["email"]
    skill_name = content["skill"]
    skill_level = content["level"]
    skill = Skill(skill_name, skill_level)
    if email in DataLayer.students:
        DataLayer.desire_skill(DataLayer.students[email], skill)
        student_name = DataLayer.students[email].get_first_name() + " " + DataLayer.students[email].get_last_name()
        response = app.response_class(
            response={
                str.format("Student {} wishes to acquire new skill {} on a level {}", student_name, skill.name, skill.level)},
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "There is no student with this email"


# edit student - the route will receive a json with the student fields.
@app.route('/students', methods=['PUT'])
def edit_field():
    content = request.json
    email = content['email']
    field = content['field']
    value = content['value']
    return DataLayer.edit_student(email, field, value)


# delete a student
@app.route('/students/<email>', methods=['DELETE'])
def delete_student(email):
    return DataLayer.remove_student(email)


# persist dictionary to a file


if __name__ == '__main__':
    app.run()
