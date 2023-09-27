from database import db

class UserRepository:
    def __init__(self):
        self.users = db["users"]

    def add_member(self, user):
        result = self.users.insert_one(user)
        return result
    
    def find_member_by_email(self, email):
        result = self.users.find_one({'email': email})
        return result
    
    def find_all_members(self):
        allmembers = self.users.find({'role': 'member'})
        return allmembers
    
    def update_member(self, email, password):
        self.users.update_one(
            {'email': email},
            {
                '$set': {
                    'password': password
                }
            }
        )