import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestOneDefaulterRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_one_defaulter(self):
        defaulter = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'unpaid'
        }
        response = self.client.post('/defaulter', data = json.dumps(defaulter), content_type = 'application/json')
        id = response.json['id']
        updated_defaulter = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'paid'
        }
        resp = self.client.put(f'/defaulter/{id}', data=json.dumps(updated_defaulter), content_type='application/json')
        self.assertEqual(resp.json['message'], 'Defaulter updated')

        id = '1234567890abcde123456789'
        resp = self.client.put(f'/defaulter/{id}', data=json.dumps(updated_defaulter), content_type='application/json')
        self.assertEqual(resp.json['message'], 'Entry not found')

    def tearDown(self):
        db['defaulters'].delete_one({'member': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()