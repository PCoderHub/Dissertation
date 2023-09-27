import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestOneBookIssueRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_update_issue(self):
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
        update_issue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'idate': '2023-08-01',
            'rdate': '2023-08-10',
            'actret': '2023-08-11',
            'status': 'returned with delay'
        }
        id = response.json['issue_id']
        resp = self.client.put(f'/issues/{id}', data = json.dumps(update_issue), content_type = 'application/json')
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        db['issues'].delete_one({'member': 'test@email.com'})
        db['books'].delete_one({'isbn13': '978-1234567890'})

if __name__ == '__main__':
    unittest.main()