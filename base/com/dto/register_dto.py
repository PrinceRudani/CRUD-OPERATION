# import re


class RegisterDTO:
    def __init__(self, register_firstname: str = None,
                 register_lastname: str = None,
                 register_gender: int = None, register_email: str = None,
                 register_username: str = None,
                 register_password: str = None):

        self.register_firstname = register_firstname
        self.register_lastname = register_lastname
        self.register_gender = register_gender
        self.register_email = register_email
        self.register_username = register_username
        self.register_password = register_password

    def validate(self):
        if not all([self.register_firstname, self.register_lastname,
                    self.register_gender, self.register_email,
                    self.register_username,
                    self.register_password]):
            raise Exception("All product fields must be filled and valid.")

        # password_pattern = re.compile(
        #     r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        # if not password_pattern.match(self.register_password):
        #     raise Exception(
        #         "Password must be at least 8 characters long, include an uppercase letter, "
        #         "a lowercase letter, a number, and a special character.")

        return self
