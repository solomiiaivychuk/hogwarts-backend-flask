import json


class Skill(dict):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return json.dumps(self.__dict__)
