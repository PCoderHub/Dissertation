import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestBooksRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_books(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            's_loc': 'T1',
            'qty': 5
        }
        response = self.client.post('/books', data = json.dumps(book), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'New book added')

        response = self.client.post('/books', data = json.dumps(book), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Book entry already exists')

    def test_get_all_books(self):
        books = self.client.get('/books')
        data = json.loads(books.data)
        self.assertEqual(len(data), 5)

    def tearDown(self):
        db['books'].delete_one({'isbn13': '978-1234567890'})

if __name__ == '__main__':
    unittest.main()