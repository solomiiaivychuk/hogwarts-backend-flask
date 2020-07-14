import json


class Skill:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return json.dumps(self.__dict__)
