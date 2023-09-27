import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestLoginRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login_member(self):
        user = {
            'firstname': 'test',
            'lastname': 'test',
            'email': 'test@email.com',
            'password': 'testtest'
        }
        response = self.client.post('/register', data = json.dumps(user), content_type = 'application/json')
        login_data = {
            'email': 'test@email.com',
            'password': 'testtest'
        }
        log_in = self.client.post('/login', data = json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(log_in.status_code, 200)
        self.assertEqual(log_in.json['message'], 'Login successful!')

        login_data['password'] = 'test1234'
        log_in = self.client.post('/login', data = json.dumps(login_data), content_type = 'application/json')
        self.assertEqual(log_in.status_code, 400)
        self.assertEqual(log_in.json['message'], 'Invalid credentials!')

    def test_get_all_members(self):
        response = self.client.get('/login')
        data = json.loads(response.data)
        self.assertEqual(len(data), 5)

    def tearDown(self):
        db['users'].delete_one({'email': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()