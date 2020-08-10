import pymongo

class MongoDataLayer:

    def __create(self):
        self.__client = pymongo.MongoClient("localhost", 27017)
        self.__db = self.__client.hogwarts
        self.__collection = self.__db.students

    def __inti__(self):
        self.create()

    #get all students from database
    def get_students_as_json(self):
        students = self.__collection.students.find()
        return students

    #get student by email
    def get_student_by_email(self, email):
        student = self.__collection.students.find({"email": email})
        return student

    #add student
    def add_student(self, data):
        try:
            self.__collection.students.insert(data)
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
            student = self.__collection.students.find({"email": email})
            self.__collection.students.delete_one(student)
            return student
        except FileNotFoundError:
            return "Student with this email does not exist in the database"


