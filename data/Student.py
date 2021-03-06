import json
from datetime import datetime
from data.Person import Person
from data.Validator import Validator


class Student(Person, dict):
    def __init__(self, email, first_name, last_name, creation_time, update_time, existing_skills,
                 desired_skills):
        super().__init__(email)
        self._first_name = first_name
        self._last_name = last_name
        self._creation_time = creation_time
        self._update_time = update_time
        self._existing_skills = existing_skills
        self._desired_skills = desired_skills

    def get_email(self):
        return self._email

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_creation_time(self):
        return self._creation_time

    def get_update_time(self):
        return self._update_time

    def get_existing_skills(self):
        ex_skills = {}
        for skill in self._existing_skills:
            ex_skills[skill.name] = {
               "skill_name": skill.name,
               "skill_level": skill.level
            }
        return ex_skills

    def get_desired_skills(self):
        des_skills = {}
        for skill in self._desired_skills:
            des_skills[skill.name] = {
                "skill_name": skill.get_name()
            }
        return des_skills

    def set_email(self, new_email):
        self._email = new_email

    def set_first_name(self, new_first_name):
        self._first_name = new_first_name

    def set_last_name(self, new_last_name):
        self._last_name = new_last_name

    def set_update_date(self, new_date):
        self._update_time = new_date

    def __str__(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, email, first_name, last_name, existing_skills, desired_skills):
        creation_time = datetime.now().__str__()[:-7]
        update_time = datetime.now().__str__()[:-7]
        new_student = cls(email, first_name, last_name, creation_time, update_time, existing_skills,
                          desired_skills)
        if Student.validate_new_student(new_student) is True:
            return new_student
        else:
            return None

    @classmethod
    def from_db(cls, email, first_name, last_name, creation_time, update_time, existing_skills, desired_skills):
        new_student = cls(email, first_name, last_name, creation_time, update_time, existing_skills,
                          desired_skills)
        if Student.validate_new_student(new_student) is True:
            return new_student
        else:
            return None

    @staticmethod
    def validate_new_student(student):
        if Validator.validate_email(student._email) is False:
            return False
        elif Validator.validate_field(student._first_name) is False:
            return False
        elif Validator.validate_field(student._last_name) is False:
            return False
        else:
            return True

    def validate_editing_student(self):
        if self is None:
            return False
        if Validator.validate_email(self._email) is False:
            return False
        elif Validator.validate_field(self._first_name) is False:
            return False
        elif Validator.validate_field(self._last_name) is False:
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
