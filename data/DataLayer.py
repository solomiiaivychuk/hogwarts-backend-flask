import json

from data.Student import Student
from data.Skill import Skill


class DataLayer:
    students = {}

    @staticmethod
    def get_students_as_dict():
        if DataLayer.students is None:
            return "The list of students does not exist"
        if len(DataLayer.students) == 0:
            return "The list of students is empty"
        else:
            return DataLayer.students

    @staticmethod
    def get_students_as_json():
        return json.dumps(DataLayer.get_students_as_dict())

    @staticmethod
    def get_student_by_email(email):
        if email not in DataLayer.students:
            return "The student with this email does not exist"
        else:
            for key, student in DataLayer.students.items():
                if student._email == email:
                    return student.__str__()

    @staticmethod
    def add_student(student):
        if student is None:
            return False
        if student._email in DataLayer.students.keys():
            return False
        DataLayer.students[student.get_email()] = student
        print(DataLayer.students)

    def add_skill(self, student, skill):
        if student.get_email() not in self._students.keys():
            return False
        self._students[student.get_email()].append_skill(skill)
        print(self)


