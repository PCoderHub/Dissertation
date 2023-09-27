import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestResetPasswordRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_reset_password(self):
        user = {
            'firstname': 'test',
            'lastname': 'test',
            'email': 'test@email.com',
            'password': 'testtest'
        }
        response = self.client.post('/register', data = json.dumps(user), content_type = 'application/json')
        data = {
            'email': 'test@email.com',
            'newpassword': '12345678'
        }
        resp = self.client.put('/resetpassword', data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(resp.json['message'], 'Password reset successful!')

        data['email'] = 'invalidtest@email.com'
        resp = self.client.put('/resetpassword', data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(resp.json['message'], 'User does not exist! Please Subscribe!')

    def tearDown(self):
        db['users'].delete_one({'email': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()