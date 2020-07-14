from data.Student import Student
from data.Skill import Skill


class DataLayer:
    def __init__(self, students={}):
        self._students = students

    def add_students(self, student):
        if student is None:
            return False
        if student.get_email() in self._students.keys():
            return False
        self._students[student.get_email()] = student
        print(self)

    def add_skill(self, student, skill):
        if student.get_email() not in self._students.keys():
            return False
        self._students[student.get_email()].add_skill(skill)
        print(self)
