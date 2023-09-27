import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestOneBookRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_book(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            's_loc': 'T1',
            'qty': 5
        }
        response = self.client.post('/books', data = json.dumps(book), content_type = 'application/json')
        id = response.json['bookId']
        resp = self.client.get(f'/books/{id}')
        self.assertEqual(resp.json['author'], 'book author')

        id = '1234567890abcde123456789'
        resp = self.client.get(f'/books/{id}')
        self.assertEqual(resp.json['message'], 'Wrong query!')

    def test_update_book(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            's_loc': 'T1',
            'qty': 5
        }
        response = self.client.post('/books', data = json.dumps(book), content_type = 'application/json')
        id = response.json['bookId']
        update_data = {
            'title': 'new book title',
            'author': 'new book author',
            'isbn13': '978-1234567890',
            's_loc': 'T2',
            'qty': 6
        }
        resp = self.client.put(f'/books/{id}', data = json.dumps(update_data), content_type = 'application/json')
        self.assertEqual(resp.json['message'], 'Book entry updated')

    def test_delete_book(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            's_loc': 'T1',
            'qty': 5
        }
        response = self.client.post('/books', data = json.dumps(book), content_type = 'application/json')
        id = response.json['bookId']
        resp = self.client.delete(f'/books/{id}')
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        db['books'].delete_one({'isbn13': '978-1234567890'})

if __name__ == '__main__':
    unittest.main()