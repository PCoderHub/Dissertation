import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestDefaulterRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_defaulter(self):
        defaulter = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'unpaid'
        }
        response = self.client.post('/defaulter', data = json.dumps(defaulter), content_type = 'application/json')
        self.assertEqual(response.json['message'], 'Defaulter added')

        defaulter['dues'] = 6
        response = self.client.post('/defaulter', data = json.dumps(defaulter), content_type = 'application/json')
        self.assertEqual(response.json['message'], 'Due updated')

        defaulter['dues'] = 0
        response = self.client.post('/defaulter', data = json.dumps(defaulter), content_type = 'application/json')
        self.assertEqual(response.json['message'], 'No dues to add')

    def test_get_all_defaulters(self):
        response = self.client.get('/defaulter')
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def tearDown(self):
        db['defaulters'].delete_one({'member': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()