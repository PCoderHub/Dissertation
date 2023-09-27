class Defaulter:
    def __init__(self, member, dues, status):
        self.__member = member
        self.__dues = dues
        self.__status = status

    def get_defaulter(self):
        return {
            "member": self.__member,
            "dues": self.__dues,
            "status": self.__status
        }