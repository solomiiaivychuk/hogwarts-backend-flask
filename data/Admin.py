from data.Person import Person


class Admin(Person):
    def __init__(self, email, password):
        super().__init__(email)
        self.__password = password


    def set_email(self, new_email):
        self._email = new_email

    def set_password(self, new_password):
        self.__password = new_password

    def get_email(self):
        return self._email

    def get_password(self):
        return self.__password

    @classmethod
    def create_admin(cls, email, password):
        new_admin = cls(email, password)
        return new_admin
