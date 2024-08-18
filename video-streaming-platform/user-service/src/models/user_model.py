from pymongo import MongoClient
from bson import ObjectId
import os
import logging

logger = logging.getLogger(__name__)

client = MongoClient(os.environ.get('MONGODB_URI'))
db = client.users

class User:
    @staticmethod
    def create(user_data):
        try:
            result = db.users.insert_one(user_data)
            logger.info(f"User created with ID: {result.inserted_id}")
            return User(str(result.inserted_id))
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def authenticate(email, password):
        try:
            user = db.users.find_one({"email": email, "password": password})
            if user:
                logger.info(f"User authenticated: {user['_id']}")
                return User(str(user['_id']))
            logger.warning(f"Authentication failed for email: {email}")
            return None
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}", exc_info=True)
            raise

    def __init__(self, id):
        self.id = id
