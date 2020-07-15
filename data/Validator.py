class Validator:

    @staticmethod
    def validate_email(email):
        at_index = email.find('@')
        dot_index = email.rfind('.')
        if email is None:
            return False
        elif type(email) != str:
            return False
        elif len(email) != len(email.split()):
            return False
        elif (len(email) - at_index) < 3:
            return False
        elif (len(email) - dot_index) < 2:
            return False
        elif dot_index - at_index < 2:
            return False
        else:
            return True

    @staticmethod
    def validate_field(field):
        if field is None:
            return False
        elif type(field) != str:
            return False
        elif len(field) == 0:
            return False
        else:
            return True

    @staticmethod
    def validate_password(password):
        if password is None:
            return False
        elif len(password) < 5:
            return False
        else:
            return True
