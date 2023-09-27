from bookRepository import BookRepository

class BookService:
    def __init__(self):
        self.bookrepo = BookRepository()

    def new_book(self, book):
        return self.bookrepo.add_book(book)
    
    def get_book(self, isbn):
        book = self.bookrepo.find_book_by_isbn(isbn)
        if book:
            return book
        return False
    
    def get_book_by_id(self, id):
        book = self.bookrepo.find_book_by_id(id)
        if book:
            return book
        return False
    
    def get_all_books(self):
        allbooks = self.bookrepo.find_all_books()
        allbooksJson = []
        for book in allbooks:
            bookDict = {
                'id': str(book['_id']),
                'title': book['title'],
                'author': book['author'],
                'isbn13': book['isbn13'],
                's_loc': book['shelfloc'],
                'qty': book['quantity']
            }

            allbooksJson.append(bookDict)

        return allbooksJson
    
    def update_book(self, book, id):
        self.bookrepo.update_book_by_id(book, id)

    def remove_book(self, id):
        self.bookrepo.delete_book(id)