import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
import json
from app import app
from database import db

class TestGenerateReportRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_generate_report(self):
        startdate = '2023-07-01'
        enddate = '2023-07-31'
        response = self.client.get(f'/generatereport?startdate={startdate}&enddate={enddate}')
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

if __name__ == '__main__':
    unittest.main()