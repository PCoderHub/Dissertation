import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestIssuesRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_new_issue(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            's_loc': 'T1',
            'qty': 5
        }
        resp = self.client.post('/books', data = json.dumps(book), content_type = 'application/json')
        issue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'idate': '2023-08-01',
            'rdate': '2023-08-10'
        }
        response = self.client.post('/issues', data = json.dumps(issue), content_type = 'application/json')
        self.assertEqual(response.json['message'], 'New issue added')
        response = self.client.post('/issues', data = json.dumps(issue), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_book_notexist(self):
        book = {
            'title': 'book title',
            'author': 'book author',
            'isbn13': '978-1234567890',
            's_loc': 'T1',
            'qty': 0
        }
        resp = self.client.post('/books', data = json.dumps(book), content_type = 'application/json')
        issue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'idate': '2023-08-01',
            'rdate': '2023-08-10'
        }
        response = self.client.post('/issues', data = json.dumps(issue), content_type = 'application/json')
        response = self.client.post('/issues', data = json.dumps(issue), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        
    def test_get_all_books(self):
        issues = self.client.get('/issues')
        data = json.loads(issues.data)
        self.assertEqual(len(data), 6)

    def tearDown(self):
        db['books'].delete_one({'isbn13' : '978-1234567890'})
        db['issues'].delete_one({'member': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()