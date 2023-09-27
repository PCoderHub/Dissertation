from defaulterRepository import DefaultRepository

class DefaultService:
    def __init__(self):
        self.defaulterrepo = DefaultRepository()

    def new_defaulter(self, defaulter):
        return self.defaulterrepo.add_defaulter(defaulter)
    
    def get_defaulter(self, member):
        defaulter = self.defaulterrepo.find_defaulter_by_member(member)
        if defaulter:
            return defaulter
        return False
    
    def get_defaulter_by_id(self, id):
        defaulter = self.defaulterrepo.find_defaulter_by_id(id)
        if defaulter:
            return defaulter
        return False
    
    def get_all_defaulters(self):
        alldefaulters = self.defaulterrepo.find_all_defaulters()
        alldefaulterJson = []
        for defaulter in alldefaulters:
            defaulterDict = {
                'id': str(defaulter['_id']),
                'member': defaulter['member'],
                'dues': defaulter['dues'],
                'status': defaulter['status']
            }
            alldefaulterJson.append(defaulterDict)

        return alldefaulterJson
    
    def update_defaulter(self, defaulter, id):
        self.defaulterrepo.update_defaulter_by_id(defaulter, id)