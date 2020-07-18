import json


class Skill(dict):
    def __init__(self, name, level):
        super().__init__()
        self.name = name
        self.level = level

    def __str__(self):
        return json.dumps(self.__dict__)

    def get_name(self):
        return self.name

    def get_level(self):
        return self.level
