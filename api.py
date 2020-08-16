from flask import Flask, request
from flask_cors import CORS, cross_origin
from data.Student import Student
from data.DataLayer import DataLayer
from data.Skill import Skill
from data.Admin import Admin
import json
import atexit
from decouple import config
from data.SqlDataLayer import SqlDataLayer
from data.MongoDataLayer import MongoDataLayer

app = Flask(__name__)
cors = CORS(app)
if config("DATABASE") == "Mysql":
    data_layer = SqlDataLayer()
elif config("DATABASE") == "MongoDB":
    data_layer = MongoDataLayer()


@app.route('/signup', methods=["POST"])
@cross_origin()
def sign_up_admin():
    content = request.json
    data_layer.add_admin(content)
    response = app.response_class(
        response={json.dumps("Success")},
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/login', methods=["POST"])
@cross_origin()
def login_admin():
    content = request.json
    admin = data_layer.login_admin(content)
    response = app.response_class(
        response=json.dumps(admin),
        status=200,
        mimetype='application/json'
    )
    return response

# get list of all students
@app.route('/students')
@cross_origin()
def get_students():
    students = data_layer.get_students()
    response = app.response_class(
        response=json.dumps(students),
        status=200,
        mimetype="application.json"
    )
    return response


# get student by email - email will be a path param
@app.route('/students/<email>')
@cross_origin()
def get_students_by_email(email):
    return data_layer.get_student_by_email(email)


# get added students per day of the year - day will be a query param
@app.route('/students/date')
@cross_origin()
def get_students_added_on_date():
    creation_year = request.args.get('year')
    creation_month = request.args.get('month')
    creation_day = request.args.get('day')
    response = []
    """"""
    return json.dumps(response)


# add a new student (request which will be invoked by admin) - the route will receive a json with the student fields.
@app.route('/students', methods=['POST'])
@cross_origin()
def add_new_student():
    content = request.json
    data_layer.add_student(content)
    response = app.response_class(
        response={json.dumps("Success")},
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
    return data_layer.edit_student(email, field, value)


# delete a student
@app.route('/students', methods=['DELETE'])
@cross_origin()
def remove_student():
    content = request.json
    print(content)
    return json.dumps(data_layer.remove_student(content['email']))

# persist dictionary to a file
@app.route('/save_dictionary')
@cross_origin()
def persist_data_to_file():
    data_layer.persist_dict_into_file()
    return "Success"

#how many students have specific skill
@app.route('/existing_skills')
@cross_origin()
def get_existing_skill():
    content = request.json
    skill = content['skill']
    return data_layer.get_students_having_specific_skill(skill)


#how many students have specific desired skill
@app.route('/desired_skills')
@cross_origin()
def get_desired_skill():
    content = request.json
    skill = content['skill']
    return data_layer.get_desired_skill(skill)


@app.route("/admins")
@cross_origin()
def get_admins():
    admins = data_layer.get_admins()
    response = app.response_class(
        response=json.dumps(admins),
        status=200,
        mimetype="application.json"
    )
    return response

if __name__ == '__main__':
    app.run()

@atexit
def exit_db():
    DataLayer.shutdown()

