from database import db
from bson.objectid import ObjectId

class DefaultRepository:
    def __init__(self):
        self.defaulters = db['defaulters']

    def add_defaulter(self, defaulter):
        result = self.defaulters.insert_one(defaulter)
        return result
    
    def find_defaulter_by_member(self, member):
        result = self.defaulters.find_one({'member': member, 'status': 'unpaid'})
        return result
    
    def find_defaulter_by_id(self, id):
        result = self.defaulters.find_one({'_id': ObjectId(id)})
        return result
    
    def find_all_defaulters(self):
        alldefaulters = self.defaulters.find()
        return alldefaulters
    
    def update_defaulter_by_id(self, defaulter, id):
        self.defaulters.update_one(
            {'_id': ObjectId(id)},
            {
                '$set': {
                    'dues': defaulter['dues'],
                    'status': defaulter['status']
                }
            }
        )