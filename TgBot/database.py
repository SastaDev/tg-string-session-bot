import pymongo
import dns

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

class MongoDB:
    def __init__(self, CONNECTION_URI):
        self.client = pymongo.MongoClient(CONNECTION_URI)

    def get_lang(self, ID):
        d = self.client['database']
        lang = d['lang']
        find = list(lang.find({'_id': 'lang'}))
        if find:
            return find[0].get(str(ID))

    def set_lang(self, ID, lang_name):
        d = self.client['database']
        lang = d['lang']
        lang.update_one({'_id': 'lang'}, {'$set': {str(ID): lang_name}}, upsert=True)

    def add_user(self, ID):
        d = self.client['string_session_database']
        users = d['total_users']
        find = list(users.find({'_id': 'total_users'}))
        if ID in find:
            return
        users.update_one({'_id': 'total_users'}, {'$set': {'user_list': [ID]}}, upsert=True)

    def get_total_users_list(self):
        d = self.client['string_session_database']
        users = d['total_users']
        find = list(users.find({'_id': 'total_users'}))
        return find

    def add_blacklist(self, ID):
        d = self.client['string_session_database']
        blacklist = d['blacklist']
        find = list(blacklist.find({'_id': 'blacklist'}))
        if ID in find:
            return
        blacklist.update_one({'_id': 'blacklist'}, {'$set': {'blacklist_list': [ID]}}, upsert=True)

    def get_blacklist_list(self):
        d = self.client['string_session_database']
        blacklist = d['blacklist']
        find = list(blacklist.find({'_id': 'blacklist'}))
        return find

    def is_blacklisted(self, ID):
        d = self.client['string_session_database']
        blacklist = d['blacklist']
        find = list(blacklist.find({'_id': 'blacklist'}))
        if ID in find:
            return True
        else:
            return False

    def remove_blacklist(self, ID):
        d = client['string_session_database']
        blacklist = d['blacklist']
        blacklist.delete_one({'blacklist_list': [ID]})

    def add_created_string_session(self, ID):
        d = self.client['string_session_database']
        ss = d['total_ss_created']
        find = list(ss.find({'_id': 'user_list'}))
        if ID in find:
            return
        ss.update_one({'_id': 'user_list'}, {'$set': {'user_list': [ID]}}, upsert=True)

    def get_total_ss_created_list(self):
        d = self.client['string_session_database']
        ss = d['total_ss_created']
        find = list(ss.find({'_id': 'user_list'}))
        return find