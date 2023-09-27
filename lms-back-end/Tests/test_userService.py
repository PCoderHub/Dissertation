import os
import sys

current = os.path.dirname(os.path.abspath(__file__)) 
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
from userService import UserService
from database import db

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.userservice = UserService()

    def test_register_member(self):
        member = {
            'firstname': 'test',
            'lastname': 'test',
            'email': 'test@email.com',
            'password': 'testtest',
            'role': 'member'
        }
        new = self.userservice.register(member)
        self.assertTrue(new)
        exist = self.userservice.register(member)
        self.assertFalse(exist)

    def test_login_valid_user(self):
        member = {
            'firstname': 'test',
            'lastname': 'test',
            'email': 'test@email.com',
            'password': 'testtest',
            'role': 'member'
        }
        self.userservice.register(member)
        valid = self.userservice.login('test@email.com', 'testtest')
        self.assertTrue(valid)
        notvalid = self.userservice.login('testinvalid@email.com', 'testtest')
        self.assertFalse(notvalid)
        
    def test_reset_password(self):
        member = {
            'firstname': 'test',
            'lastname': 'test',
            'email': 'test@email.com',
            'password': 'testtest',
            'role': 'member'
        }
        self.userservice.register(member)
        reset = self.userservice.reset_password('test@email.com', 'test1234')
        self.assertTrue(reset)
        result = self.userservice.reset_password('testinvalid@email.com', 'testtest')
        self.assertFalse(result)

    def test_get_all_members(self):
       result = self.userservice.get_all_members()
       self.assertEqual(len(result), 5)

    def tearDown(self):
        db['users'].delete_one({'email': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()