class User:
    def __init__(self, firstname, lastname, email, password, role):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email
        self.__password = password
        self.__role = role

    def get_user(self):
        return {
            'firstname': self.__firstname,
            'lastname': self.__lastname,
            'email': self.__email,
            'password': self.__password,
            'role': self.__role
        }