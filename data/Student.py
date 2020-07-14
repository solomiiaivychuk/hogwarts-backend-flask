import json
from datetime import datetime
from data.Person import Person


class Student(Person):
    def __init__(self, id_num, first_name, last_name, email, password, creation_time, update_time, existing_skills=[],
                 desired_skills=[]):
        super().__init__(id_num, first_name, last_name, email, password)
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

    @classmethod
    def from_json(cls, id_num, first_name, last_name, email, password):
        existing_skills = []
        desired_skills = []
        creation_date = datetime.now()
        update_time = ""
        st_instance = cls(id_num, first_name, last_name, email, password, creation_date, update_time, existing_skills, desired_skills)
        return json.loads(st_instance.__str__())


