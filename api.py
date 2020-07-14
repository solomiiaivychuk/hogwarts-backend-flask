from flask import Flask, request

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


# get list of all students
@app.route('/students')
def get_all_students():
    return


# get student by email - email will be a path param
@app.route('/students/<email>')
def get_students_by_email(email):
    return


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
@app.route('/students/add', methods=['POST'])
def add_new_student():
    return


# login a student(email + password) - the route will receive a json with the data.
@app.route('/students', methods=['POST'])
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