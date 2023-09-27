import os
import sys

current = os.path.dirname(os.path.abspath(__file__)) 
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
from issueService import IssueService
from database import db

class TestIssueService(unittest.TestCase):
    def setUp(self):
        self.issueservice = IssueService()

    def test_add_new_issue(self):
        issue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'issuedate': '2023-08-02',
            'returndate': '2023-08-10',
            'actualreturn': '',
            'status': 'pending'
        }
        result = self.issueservice.add_new_issue(issue)
        self.assertTrue(result)

    def test_get_issue(self):
        issue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'issuedate': '2023-08-02',
            'returndate': '2023-08-10',
            'actualreturn': '',
            'status': 'pending'
        }
        self.issueservice.add_new_issue(issue)
        exist = self.issueservice.get_issue('test@email.com')
        self.assertTrue(exist)
        notexist = self.issueservice.get_issue('testinvalid@email.com')
        self.assertFalse(notexist)

        issue1 = {
            'book': '978-1234567890',
            'member': 'test1@email.com',
            'issuedate': '2023-08-02',
            'returndate': '2023-08-10',
            'actualreturn': '2023-08-05',
            'status': 'returned'
        }
        self.issueservice.add_new_issue(issue1)
        result = self.issueservice.get_issue('test1@email.com')
        self.assertFalse(result)

    def test_get_issue_by_id(self):
        issue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'issuedate': '2023-08-02',
            'returndate': '2023-08-10',
            'actualreturn': '',
            'status': 'pending'
        }
        i = self.issueservice.add_new_issue(issue)
        result = self.issueservice.get_issue_by_id(str(i.inserted_id))
        self.assertTrue(result)
        wrongid = self.issueservice.get_issue_by_id('1234567890abcde123456789')
        self.assertFalse(wrongid)

    def test_get_all_issues(self):
        result = self.issueservice.get_all_issues()
        self.assertEqual(len(result), 6)

    def test_update_issue(self):
        issue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'issuedate': '2023-08-02',
            'returndate': '2023-08-10',
            'actualreturn': '',
            'status': 'pending'
        }
        i = self.issueservice.add_new_issue(issue)
        updatedissue = {
            'book': '978-1234567890',
            'member': 'test@email.com',
            'issuedate': '2023-08-02',
            'returndate': '2023-08-10',
            'actualreturn': '2023-08-05',
            'status': 'returned'
        }
        self.issueservice.update_issue(updatedissue, str(i.inserted_id))
        result = self.issueservice.get_issue_by_id(str(i.inserted_id))
        self.assertEqual(result['actualreturn'], '2023-08-05')
        self.assertEqual(result['status'], 'returned')

    def test_generate_report(self):
        result = self.issueservice.generate_report('2023-07-01', '2023-07-31')
        self.assertEqual(len(result), 3)
    
    def tearDown(self):
        db['issues'].delete_many({'book': '978-1234567890'})

if __name__ == '__main__':
    unittest.main()