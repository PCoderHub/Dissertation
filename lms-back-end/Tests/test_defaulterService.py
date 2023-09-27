import os
import sys

current = os.path.dirname(os.path.abspath(__file__)) 
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
from defaulterService import DefaultService
from database import db

class TestDefaultService(unittest.TestCase):
    def setUp(self):
        self.defaultservice = DefaultService()

    def test_new_defaulter(self):
        defaulter = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'unpaid'
        }
        result = self.defaultservice.new_defaulter(defaulter)
        self.assertTrue(result)

    def test_get_defaulter(self):
        defaulter = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'unpaid'
        }
        self.defaultservice.new_defaulter(defaulter)
        exist = self.defaultservice.get_defaulter('test@email.com')
        self.assertTrue(exist)
        notexist = self.defaultservice.get_defaulter('testinvalid@email.com')
        self.assertFalse(notexist)

    def test_get_defaulter_by_id(self):
        defaulter = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'unpaid'
        }
        d = self.defaultservice.new_defaulter(defaulter)
        right = self.defaultservice.get_defaulter_by_id(str(d.inserted_id))
        self.assertTrue(right)
        wrong = self.defaultservice.get_defaulter_by_id('1234567890abcde123456789')
        self.assertFalse(wrong)

    def test_get_all_defaulters(self):
        result = self.defaultservice.get_all_defaulters()
        self.assertEqual(len(result), 2)

    def test_update_defaulter(self):
        defaulter = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'unpaid'
        }
        d = self.defaultservice.new_defaulter(defaulter)
        updated = {
            'member': 'test@email.com',
            'dues': 5,
            'status': 'paid'
        }
        self.defaultservice.update_defaulter(updated, str(d.inserted_id))
        result = self.defaultservice.get_defaulter_by_id(str(d.inserted_id))
        self.assertEqual(result['status'], 'paid')

    def tearDown(self):
        db['defaulters'].delete_one({'member': 'test@email.com'})

if __name__ == '__main__':
    unittest.main()