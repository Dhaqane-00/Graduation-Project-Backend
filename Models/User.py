from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB URL from the environment variables
MONGODB_URL = os.getenv('MONGODB_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize the MongoDB client with the Atlas connection string
client = MongoClient(MONGODB_URL)
db = client['predictions_db']
users_collection = db['users']

class User:
    def __init__(self, name, email, password, role='User', status='Active', image='default.jpg', _id=None):
        if _id is None:
            self._id = ObjectId()
        else:
            self._id = _id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.status = status
        self.image = image

    def save_to_db(self):
        users_collection.insert_one(self.__dict__)

    def update_in_db(self):
        users_collection.update_one({'_id': self._id}, {'$set': self.__dict__})

    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": user_id})

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def delete_by_id(user_id):
        users_collection.delete_one({"_id": user_id})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    @staticmethod
    def generate_token(email, role, status):
        payload = {
            'email': email,
            'role': role,
            'status': status,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    
    def generate_reset_token(self):
        payload = {
            'email': self.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }
        return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            email = payload.get('email')  # Get the email from the token payload
            exp = payload.get('exp')  # Get the expiration time from the token payload
            # Check if the token has expired
            if datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(exp):
                return None  # Token expired
            return email
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    @staticmethod
    def reset_password(email, new_password):
        hashed_password = generate_password_hash(new_password)
        users_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
