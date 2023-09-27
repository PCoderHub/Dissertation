from userRepository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def __init__(self):
        self.userrepo = UserRepository()

    def register(self, user):
        user['password'] = generate_password_hash(user['password'])
        existinguser = self.userrepo.find_member_by_email(user['email'])
        if existinguser:
            return False
        return self.userrepo.add_member(user)
    
    def login(self, email, password):
        user = self.userrepo.find_member_by_email(email)
        if user:
            pw = check_password_hash(user['password'], password)
            if pw:
                return user
            else:
                return False
        return False
    
    def get_all_members(self):
        allmembers = self.userrepo.find_all_members()
        allmembersJson = []
        for member in allmembers:
            memberDict = {
                'id': str(member['_id']),
                'firstname': member['firstname'],
                'lastname': member['lastname'],
                'email': member['email']
            }
            allmembersJson.append(memberDict)
        
        return allmembersJson
    
    def reset_password(self, email, password):
        user = self.userrepo.find_member_by_email(email)
        new_password = generate_password_hash(password)
        if user:
            self.userrepo.update_member(email, new_password)
            return True
        return False
