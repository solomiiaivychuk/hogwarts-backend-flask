import json

from data.Student import Student
from data.Skill import Skill


class DataLayer:
    students = {}

    def get_students(self):
        if self._students is None:
            return "The list of students does not exist"
        if len(self._students) == 0:
            return "The list of students is empty"
        else:
            return json.dumps(self._students)

    def get_student_by_email(self, email):
        if email not in self._students.keys():
            return "The student with this email does not exist"
        else:
            for s in self._students:
                if s._email == email:
                    return self._students[s]

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


