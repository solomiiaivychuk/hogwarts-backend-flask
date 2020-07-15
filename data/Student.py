import json
from datetime import datetime
from data.Person import Person
from data.Validator import Validator


class Student(Person, dict):
    def __init__(self, id_num, first_name, last_name, email, password, creation_time, update_time, existing_skills=[],
                 desired_skills=[]):
        super().__init__(id_num, first_name, last_name, email)
        self.__password = password
        self._creation_time = creation_time
        self._update_time = update_time
        self._existing_skill = existing_skills
        self._desired_skills = desired_skills

    def get_id(self):
        return self._id_num

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_email(self):
        return self._email

    def get_password(self):
        return self.__password

    def get_creation_time(self):
        return self._creation_time

    def get_update_time(self):
        return self._update_time

    def get_existing_skills(self):
        return self._existing_skill

    def get_desired_skills(self):
        return self._desired_skills

    def __str__(self):
        return json.dumps(self.__dict__)

    def append_skill(self, skill):
        self._existing_skill.append(skill)

    def wish_skill(self, skill):
        self._desired_skills.append(skill)

    @classmethod
    def from_json(cls, id_num, first_name, last_name, email, password):
        existing_skills = []
        desired_skills = []
        creation_date = datetime.now().__str__()[:-7]
        update_time = datetime.now().__str__()[:-7]
        new_student = cls(id_num, first_name, last_name, email, password, creation_date, update_time, existing_skills, desired_skills)
        if Student.validate_new_student(new_student) is True:
            return new_student
        else:
            return None

    @staticmethod
    def validate_new_student(student):
        if Validator.validate_email(student._email) is False:
            return False
        elif Validator.validate_field(student._last_name) is False:
            return False
        elif Validator.validate_field(student._id_num) is False:
            return False
        elif Validator.validate_field(student.__password) is False:
            return False
        else:
            return True


    def validate_login_student(self):
        if Validator.validate_field(self._email) is False:
            return False
        elif Validator.validate_field(self.__password) is False:
            return False
        else:
            return True

    def validate_existing_student(self):
        if self is None:
            return False
        if Validator.validate_email(self._email) is False:
            return False
        elif Validator.validate_field(self._last_name) is False:
            return False
        elif Validator.validate_password(self.__password) is False:
            return False
        else:
            return True

    def validate_getting_by_email(self):
        if Validator.validate_field(self._email) is False:
            return False
        else:
            return True

    def validate_date(self):
        if Validator.validate_field(self._creation_time) is False:
            return False
        else:
            return True
