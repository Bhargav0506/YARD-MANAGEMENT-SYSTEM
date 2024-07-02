# database.py
from pymongo import MongoClient

class Database:
    def __init__(self):
        # Connect to MongoDB using the admin credentials
        self.client = MongoClient("mongodb://admin:password@localhost:27017/?authSource=admin")
        self.db = self.client['yard_management']

    def get_collection(self, name):
        return self.db[name]
