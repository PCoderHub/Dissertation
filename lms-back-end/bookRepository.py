from database import db
from bson.objectid import ObjectId

class BookRepository:
    def __init__(self):
        self.books = db["books"]

    def add_book(self, book):
        result = self.books.insert_one(book)
        return result
    
    def find_book_by_isbn(self, isbn):
        result = self.books.find_one({'isbn13': isbn})
        return result

    def find_book_by_id(self, id):
        result = self.books.find_one({'_id': ObjectId(id)})
        return result
    
    def find_all_books(self):
        allbooks = self.books.find()
        return allbooks
    
    def update_book_by_id(self, book, id):
        self.books.update_one(
            {'_id': ObjectId(id)},
            {
                '$set': {
                    'title': book['title'],
                    'author': book['author'],
                    'isbn13': book['isbn13'],
                    'shelfloc': book['shelfloc'],
                    'quantity': book['quantity']
                }
            }
        )

    def delete_book(self, id):
        self.books.delete_many({'_id': ObjectId(id)})