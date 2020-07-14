from data.Person import Person


class Professor(Person):
    def __init__(self, id_num, first_name, last_name, email, password):
        super().__init__()
