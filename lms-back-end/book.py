class Book:
    def __init__(self, title, author, isbn13, s_loc, qty):
        self.__title = title
        self.__author = author
        self.__isbn13 = isbn13
        self.__s_loc = s_loc
        self.__qty = qty

    def get_book(self):
        return {
            'title': self.__title,
            'author': self.__author,
            'isbn13': self.__isbn13,
            'shelfloc': self.__s_loc,
            'quantity': self.__qty
        }