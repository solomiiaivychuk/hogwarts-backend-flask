from flask import Flask, request
from flask_cors import CORS, cross_origin
from data.Student import Student
from data.DataLayer import DataLayer
from data.Skill import Skill
from data.Admin import Admin
import json
import atexit

app = Flask(__name__)
cors = CORS(app)

"""
# load dictionary from a file
@app.before_first_request
def load_data_from_file():
    return DataLayer.load_dict_from_file()
"""


@app.route('/signup', methods=["POST"])
@cross_origin()
def sign_up_admin():
    content = request.json
    admin = Admin(content['email'], content['password'])
    DataLayer.add_new_admin(admin)
    response = app.response_class(
        response={json.dumps(admin.__dict__)},
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/login', methods=["POST"])
@cross_origin()
def login_admin():
    content = request.json
    email = content['email']
    password = content['password']
    if email in DataLayer.admins:
        if password == DataLayer.admins[email].get_password():
            response = app.response_class(
                response={json.dumps("Logged in successfully")},
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            return "Wrong password"
    else:
        return "The admin with this email does not exist"


# get list of all students
@app.route('/students')
@cross_origin()
def get_all_students():
    return DataLayer.get_students_as_json()


# get student by email - email will be a path param
@app.route('/students/<email>')
@cross_origin()
def get_students_by_email(email):
    return DataLayer.get_student_by_email(email)


# get added students per day of the year - day will be a query param
@app.route('/students/date')
@cross_origin()
def get_students_added_on_date():
    creation_year = request.args.get('year')
    creation_month = request.args.get('month')
    creation_day = request.args.get('day')
    response = []
    for student in DataLayer.students.values():
        if creation_year == student._creation_time[:4] and \
                creation_month == student._creation_time[5:7] and \
                creation_day == student._creation_time[8:10]:
            response.append(student.__dict__)
        else:
            response = str.format("No students were added on {}-{}-{}", creation_year, creation_month, creation_day)
    return json.dumps(response)


# get count of desired skills (how many of the students desire a specific skill)
@app.route('/skills/wish')
@cross_origin()
def get_desirable_skill():
    skill = request.args.get('skill')
    return DataLayer.get_desired_skill(skill)


# get count for how many students have each type of skill
@app.route('/skills/acquire')
@cross_origin()
def get_existing_skills():
    skill = request.args.get('skill')
    return DataLayer.get_existing_skill(skill)


# add a new student (request which will be invoked by admin) - the route will receive a json with the student fields.
@app.route('/students', methods=['POST'])
@cross_origin()
def add_new_student():
    content = request.json
    student = Student.from_json(content['email'], content['first_name'], content['last_name'],
                                content['existing_skills'], content['desired_skills'])
    DataLayer.add_student(content)
    response = app.response_class(
        response={json.dumps(student.__dict__)},
        status=200,
        mimetype='application/json'
    )
    return response

# edit student - the route will receive a json with the student fields.
@app.route('/students', methods=['PUT'])
@cross_origin()
def edit_field():
    content = request.json
    email = content['email']
    field = content['field']
    value = content['value']
    return DataLayer.edit_student(email, field, value)


# delete a student
@app.route('/students', methods=['DELETE'])
@cross_origin()
def delete_student():
    content = request.json
    print(str.format("Deleting ", content))
    return DataLayer.remove_student(content)

# persist dictionary to a file
@app.route('/save_dictionary')
@cross_origin()
def persist_data_to_file():
    DataLayer.persist_dict_into_file()
    return "Success"


if __name__ == '__main__':
    app.run()


@atexit
def exit_db():
    DataLayer.shutdown()
