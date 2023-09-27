import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestRegisterRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_register_member(self):
        user = {
            'firstname': 'test',
            'lastname': 'test',
            'email': 'test@email.com',
            'password': 'testtest'
        }
        response = self.client.post('/register', data = json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'New member added')

        response = self.client.post('/register', data = json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'User already exists')

    def tearDown(self):
        db['users'].delete_one({'email': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()