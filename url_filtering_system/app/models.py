# app/models.py
from datetime import datetime

class URL:
    def __init__(self, db):
        self.collection = db['urls']
        self.history_collection = db['url_history']
    
    def add_url(self, url, action, user):
        timestamp = datetime.now()
        
        # Add to history
        history_entry = {
            'name': user,
            'url': url,
            'action': action,
            'time': timestamp.strftime('%H:%M:%S'),
            'date': timestamp.strftime('%Y-%m-%d')
        }
        self.history_collection.insert_one(history_entry)
        
        # Update active URLs
        if action == 'allow':
            self.collection.update_one(
                {'url': url},
                {'$set': {'action': 'allowed', 'updated_by': user, 'updated_at': timestamp}},
                upsert=True
            )
        else:
            self.collection.update_one(
                {'url': url},
                {'$set': {'action': 'blocked', 'updated_by': user, 'updated_at': timestamp}},
                upsert=True
            )
    
    def get_active_urls(self):
        return list(self.collection.find({}, {'_id': 0}))
    
    def get_history(self, user=None):
        if user:
            return list(self.history_collection.find({'name': user}, {'_id': 0}))
        return list(self.history_collection.find({}, {'_id': 0}))