from data.Person import Person


class Professor(Person):
    def __init__(self, email, password):
        super().__init__(email)
        self.__password = password
