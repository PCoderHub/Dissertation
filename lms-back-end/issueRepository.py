from database import db
from bson.objectid import ObjectId
from datetime import datetime

class IssueRepository:
    def __init__(self):
        self.issues = db["issues"]

    def add_issued(self, issue):
        result = self.issues.insert_one(issue)
        return result
    
    def find_issue_by_member(self, email):
        result = self.issues.find_one({'member': email, '$or': [{'actualreturn': ''},{'status': 'returned with delay'}]})
        return result
    
    def find_issue_by_id(self, id):
        result = self.issues.find_one({'_id': ObjectId(id)})
        return result
    
    def find_all_issues(self):
        allissues = self.issues.find()
        return allissues
    
    def update_issue_by_id(self, issue, id):
        self.issues.update_one(
            {'_id': ObjectId(id)},
            {
                '$set': {
                    "book": issue['book'],
                    "member": issue['member'],
                    "issuedate": issue['issuedate'],
                    "returndate": issue['returndate'],
                    "actualreturn": issue['actualreturn'],
                    "status": issue['status']
                }
            }
        )

    def get_report(self, startdate, enddate):
        data = self.issues.find({
            'issuedate': { '$gte': startdate, '$lte': enddate},
        })
        return data