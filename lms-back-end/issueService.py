from issueRepository import IssueRepository

class IssueService:
    def __init__(self):
        self.issuerepo = IssueRepository()

    def add_new_issue(self, issue):
        return self.issuerepo.add_issued(issue)

    def get_issue(self, email):
        issue = self.issuerepo.find_issue_by_member(email)
        if issue:
            return issue
        return False
    
    def get_issue_by_id(self, id):
        issue = self.issuerepo.find_issue_by_id(id)
        if issue:
            return issue
        return False
    
    def get_all_issues(self):
        allissues = self.issuerepo.find_all_issues()
        allissuesJson = []

        for issue in allissues:
            issueDict = {
                'id': str(issue['_id']),
                'book': issue['book'],
                'member': issue['member'],
                'idate': issue['issuedate'],
                'rdate': issue['returndate'],
                'actret': issue['actualreturn'],
                'status': issue['status']
            }

            allissuesJson.append(issueDict)
        return allissuesJson
    
    def update_issue(self, issue, id):
        self.issuerepo.update_issue_by_id(issue, id)

    def generate_report(self, startdate, enddate):
        report = self.issuerepo.get_report(startdate, enddate)
        reportData = []

        for rep in report:
            reportDict = {
                'id': str(rep['_id']),
                'book': rep['book'],
                'member': rep['member'],
                'idate': str(rep['issuedate']),
                'rdate': str(rep['returndate']),
                'actret': str(rep['actualreturn']),
                'status': rep['status']
            }
            reportData.append(reportDict)
        return reportData