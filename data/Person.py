import json


class Person:
    def __init__(self, email):
        self._email = email

    def __str__(self):
        return json.dumps(self.__dict__)
