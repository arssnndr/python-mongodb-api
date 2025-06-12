import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.mongodb_url = os.getenv("MONGODB_URL")
        self.database_name = os.getenv("DATABASE_NAME")
        self.client = None
        self.database = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.mongodb_url)
            self.database = self.client[self.database_name]
            # Test connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return False
    
    def get_collection(self, collection_name):
        """Get a collection from the database"""
        if self.database is not None:
            return self.database[collection_name]
        else:
            raise Exception("Database not connected")
    
    def close_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("Database connection closed")

# Create database instance
db = Database()

