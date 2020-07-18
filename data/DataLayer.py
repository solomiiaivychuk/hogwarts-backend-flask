import json
from datetime import datetime

from data.Student import Student
from data.Skill import Skill


class DataLayer:
    students = {}

    # function for receiving all students within the dictionary
    @staticmethod
    def get_students_as_dict():
        temp = {}
        if DataLayer.students is None:
            return "The list of students does not exist"
        if len(DataLayer.students) == 0:
            return "The list of students is empty"
        else:
            for email, student in DataLayer.students.items():
                temp[email] = {
                    "id": student.get_id(),
                    "first_name": student.get_first_name(),
                    "last_name": student.get_last_name(),
                    "email": student.get_email(),
                    "creation_time": student.get_creation_time(),
                    "update_time": student.get_update_time(),
                    "existing_skills": student.get_existing_skills(),
                    "desired_skills": student.get_desired_skills(),
                }
            return temp

    # function for receiving all students within the dictionary as json strings. The function will call
    # the previous function and afterwards convert the returned data to be a list of json strings
    @staticmethod
    def get_students_as_json():
        return json.dumps(DataLayer.get_students_as_dict())

    # function for getting a specific student from the dictionary by its email.
    @staticmethod
    def get_student_by_email(email):
        if email not in DataLayer.students:
            return "The student with this email does not exist"
        else:
            for key, student in DataLayer.students.items():
                if student.get_email() == email:
                    return student.__str__()

    # function for setting a specific student to the dictionary by its email
    @staticmethod
    def add_student(student):
        if student is None:
            return "No student to add"
        elif student.get_email() in DataLayer.students:
            return "The student with this email exists"
        else:
            DataLayer.students[student.get_email()] = student
            print(DataLayer.students)

    @staticmethod
    def add_skill(student, skill):
        if student.get_email() not in DataLayer.students.keys():
            return "The student with this email does not exist in the database"
        else:
            student._update_time = datetime.now().__str__()[:-7]
            DataLayer.students[student.get_email()].append_skill(skill)

    @staticmethod
    def desire_skill(student, skill):
        if student.get_email() not in DataLayer.students.keys():
            return "The student with this email does not exist in the database"
        else:
            student._update_time = datetime.now().__str__()[:-7]
            DataLayer.students[student.get_email()].wish_skill(skill)

    # function for removing a student from the students dictionary
    @staticmethod
    def remove_student(email):
        if email not in DataLayer.students.keys():
            return "The student with this email does not exist in the database"
        else:
            DataLayer.students.pop(email)
            return str.format("Deleted {} successfully", email)

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

    # function for loading the data from students.json, converting it to students class instances
    # and populating the instances into the students dictionary object of the DataLayer class
    @staticmethod
    def load_dict_from_file():
        try:
            with open('.\\data\\students.json', 'r') as read_file:
                if DataLayer.students is None:
                    return "The dictionary does not exist"
                else:
                    DataLayer.students = json.load(read_file)
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

# get count for how many students have each type of skill
    @staticmethod
    def get_existing_skill(skill):
        count = 0
        for key, student in DataLayer.students.items():
            for existing_skill in student.get_existing_skills():
                if existing_skill == skill:
                    count += 1
        return str.format('{} students have the skill "{}"', count, skill)

# get count of desired skills (how many of the students desire a specific skill)
    @staticmethod
    def get_desired_skill(skill):
        count = 0
        for key, student in DataLayer.students.items():
            for desired_skill in student.get_desired_skills():
                if desired_skill == skill:
                    count += 1
        return str.format('{} students wish to have the skill "{}"', count, skill)
