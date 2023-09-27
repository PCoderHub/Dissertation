class Issue:
    def __init__(self, book, member, iDate, rDate, actualreturn, status):
        self.__book = book
        self.__member = member
        self.__iDate = iDate
        self.__rDate = rDate
        self.__status = status
        self.__actualreturn = actualreturn

    def get_issue(self):
        return {
            "book": self.__book,
            "member": self.__member,
            "issuedate": self.__iDate,
            "returndate":self.__rDate,
            "actualreturn": self.__actualreturn,
            "status": self.__status
        }