import json
from datetime import datetime
from data.MongoDataLayer import MongoDataLayer
from data.Student import Student
from data.Skill import Skill

mongo_db = MongoDataLayer()


class DataLayer:

    # function for receiving all students within the dictionary
    @staticmethod
    def get_students_as_dict():
        return mongo_db.get_students_as_dict()

    # function for receiving all students within the dictionary as json strings. The function will call
    # the previous function and afterwards convert the returned data to be a list of json strings
    @staticmethod
    def get_students_as_json():
        return mongo_db.get_students_as_json()

    # function for getting a specific student from the dictionary by its email.
    @staticmethod
    def get_student_by_email(email):
        return mongo_db.get_student_by_email(email)

    # function for setting a specific student to the dictionary by its email
    @staticmethod
    def add_student(student):
        mongo_db.add_student(student)
        return "Added student successfully"

    # function for removing a student from the students dictionary
    @staticmethod
    def remove_student(email):
        try:
            mongo_db.remove_student(email)
            return str.format("Deleted {} successfully", email)
        except OSError:
            return "Cannot delete doc"

    # function for persisting all the students' class instances in the dictionary into a json file
    @staticmethod
    def persist_dict_into_file():
        try:
            with open('.\\data\\students.json', 'w') as write_file:
                if DataLayer.students is None:
                    return "The dictionary does not exist"
                else:
                    json.dump(DataLayer.get_students_as_dict(), write_file)
                    return "Added dictionary into the file successfully"
        except FileNotFoundError:
            return "File not found"

    """
    function for loading the data from students.json, converting it to students class instances
    and populating the instances into the students dictionary object of the DataLayer class
    1. get data from file
    2. loop over each item
    3. loop over existing skills of each student
        3.1 create instance of the skill
        3.2 add skills to the existing skills dictionary
    4. loop over desired skills of each student
        3.1 create instance of the skill
        3.2 add skills to the desired skills dictionary
    5. create instance of the student using data from the json file
    6. add dictionaries with the skills to the instance
    7. add each student to the dictionary
    """
    @staticmethod
    def load_dict_from_file():
        temp = {}
        temp_ex_skills = {}
        temp_des_skills = {}
        try:
            with open('.\\data\\students.json', 'r') as read_file:
                temp_stud = json.load(read_file)
                for email, student in temp_stud.items():
                    for skill_name, skill_value in student['existing_skills'].items():
                        ex_skill = Skill(skill_value['skill_name'], skill_value['skill_level'])
                        temp_ex_skills[skill_name] = {
                            "skill_name": ex_skill.get_name(),
                            "skill_level": ex_skill.get_level()
                        }
                        for des_skill_name, des_skill_value in student['desired_skills'].items():
                            des_skill = Skill(des_skill_value['skill_name'], des_skill_value['skill_level'])
                            temp_des_skills[des_skill_name] = {
                                "skill_name": des_skill.get_name()
                            }
                    stud = Student.from_file(student['id'], student['first_name'], student['last_name'],
                                             student['email'], student['password'], student['creation_time'],
                                             student['update_time'], temp_ex_skills,
                                             temp_des_skills)

                    DataLayer.students[email] = {
                        "id": stud.get_id(),
                        "first_name": stud.get_first_name(),
                        "last_name": stud.get_last_name(),
                        "email": stud.get_email(),
                        "password": stud.get_password(),
                        "creation_time": stud.get_creation_time(),
                        "update_time": stud.get_update_time(),
                        "existing_skills": stud._existing_skills,
                        "desired_skills": stud._desired_skills,
                    }
            return DataLayer.students
        except FileNotFoundError:
            return "File not found"

    @staticmethod
    def edit_student(email, field, value):
        if email in DataLayer.students:
            if field == 'first_name':
                DataLayer.students[email].set_first_name(value)
            elif field == 'last_name':
                DataLayer.students[email].set_last_name(value)
            elif field == 'password':
                DataLayer.students[email].set_password(value)
            DataLayer.students[email].set_update_date(datetime.now().__str__()[:-7])
            return "Edited student successfully"
        else:
            return "The email is not in the students database"

    #how many students have specific skill
    @staticmethod
    def get_existing_skill(skill):
        return mongo_db.get_existing_skill_mongo(skill)

    #how many students have specific desired skill
    @staticmethod
    def get_desired_skill(skill):
        return mongo_db.get_desired_skill_mongo(skill)

