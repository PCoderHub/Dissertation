import os
import sys

current = os.path.dirname(os.path.abspath(__file__)) 
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
from bookService import BookService
from database import db

class TestBookService(unittest.TestCase):
    def setUp(self):
        self.bookservice = BookService()

    def test_new_book(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            'shelfloc': 'T1',
            'quantity': 5
        }
        result = self.bookservice.new_book(book)
        self.assertTrue(result)

    def test_get_book(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            'shelfloc': 'T1',
            'quantity': 5
        }
        self.bookservice.new_book(book)
        exist = self.bookservice.get_book('978-1234567890')
        self.assertTrue(exist)
        notexist = self.bookservice.get_book('978-0101010101')
        self.assertFalse(notexist)

    def test_get_book_by_id(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            'shelfloc': 'T1',
            'quantity': 5
        }
        b = self.bookservice.new_book(book)
        exist = self.bookservice.get_book_by_id(str(b.inserted_id))
        self.assertTrue(exist)
        notexist = self.bookservice.get_book_by_id('1234567890abcdef12345678')
        self.assertFalse(notexist)

    def test_update_book(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            'shelfloc': 'T1',
            'quantity': 5
        }
        r = self.bookservice.new_book(book)
        updatedbook = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            'shelfloc': 'T2',
            'quantity': 6
        }
        self.bookservice.update_book(updatedbook, str(r.inserted_id))
        result = self.bookservice.get_book_by_id(str(r.inserted_id))
        self.assertEqual(result['shelfloc'], 'T2')
        self.assertEqual(result['quantity'], 6)

    def test_remove_book(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            'shelfloc': 'T1',
            'quantity': 5
        }
        r = self.bookservice.new_book(book)
        self.bookservice.remove_book(str(r.inserted_id))
        result = self.bookservice.get_book_by_id(str(r.inserted_id))
        self.assertFalse(result)

    def test_get_all_books(self):
        result = self.bookservice.get_all_books()
        self.assertEqual(len(result), 5)

    def tearDown(self):
        db['books'].delete_one({'isbn13': '978-1234567890'})

if __name__ == '__main__':
    unittest.main()