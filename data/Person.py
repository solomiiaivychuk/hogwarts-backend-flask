import json


class Person:
    def __init__(self, id_num, first_name, last_name, email, password):
        self._id_num = id_num
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self.__password = password

    def __str__(self):
        return json.dumps(self.__dict__)
