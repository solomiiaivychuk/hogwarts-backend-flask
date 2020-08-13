import pymongo
from flask import json
from data.Student import Student
from data.DataLayer import DataLayer


class MongoDataLayer(DataLayer):

    def __connect(self):
        self.__client = pymongo.MongoClient("localhost", 27017)
        self.__db = self.__client.hogwarts
        self.__collection = self.__db.students

    def close(self):
        self.__client.close()

    def __init__(self):
        super().__init__()
        self.__connect()

    #get all students as dictionary
    def get_students_as_dict(self):
        students_dict = {}
        students = self.__db.students.find()
        for student in students:
            students_dict[student["email"]] = {
                "email": student["email"],
                "first_name": student["first_name"],
                "last_name": student["last_name"],
                "existing_skills": student["existing_skills"],
                "desired_skills": student["desired_skills"]
            }
        return students_dict

    #get all students as json
    def get_students(self):
        return self.get_students_as_dict()


    #get student by email
    def get_student_by_email(self, email_param):
        student_dict = {}
        data = self.__db.students.find({"email": email_param})
        email = ''
        first_name = ''
        last_name = ''
        existing_skills = []
        desired_skills = []

        for property in data:
            student_dict[property["email"]] = {
                "email": property['email'],
                "first_name": property["first_name"],
                "last_name": property["last_name"],
                "existing_skills": property["existing_skills"],
                "desired_skills": property["desired_skills"],
            }
        student = Student.from_json(email, first_name, last_name, existing_skills, desired_skills)
        print(student)
        return json.dumps(student_dict)

    #add student
    def add_student(self, data):
        try:
            self.__db.students.insert(data)
            return "Success"
        except OSError:
            return "Error occured"

    #edit student by email
    def edit_student(self, email, field, value):
        student = self.__collection.students.find({"email": email})
        if field == "first_name":
            self.__collection.students.update({"email": email}, {"$set": {"first_name": value}})
        if field == "last_name":
            self.__collection.students.update({"email": email}, {"$set": {"last_name": value}})
        if field == "existing_skills":
            self.__collection.students.update({"email": email}, {"$set": {"existing_skills": value}})
        if field == "desired_skills":
            self.__collection.students.update({"email": email}, {"$set": {"desired_skills": value}})

    #delete student by email
    def remove_student(self, email):
        try:
            self.__db.students.delete_one(email)
            return "Success"
        except FileNotFoundError:
            return "Student with this email does not exist in the database"

    def shutdown(self):
        self.__client.close()

    #how many students have specific skill
    def get_existing_skill_mongo(self, skill):
        pipeline = [{"$match": {"existing_skills.name": skill}}, {"$count": "num_of_students"}]
        value = list(self.__db.students.aggregate(pipeline))
        response = ''
        for prop in value:
            response = prop
        return json.dumps(response)

        # how many students have specific skill

    def get_desired_skill_mongo(self, skill):
        pipeline = [{"$match": {"desired_skills.name": skill}}, {"$count": "num_of_students"}]
        value = list(self.__db.students.aggregate(pipeline))
        for prop in value:
            print(prop)
            return json.dumps(prop)

