from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client['predictions_db']
users_collection = db['users']

class User:
    def __init__(self, name, email, password, role='User', status='Active', image='default.jpg'):
        self._id = ObjectId()
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.status = status
        self.image = image

    def save_to_db(self):
        users_collection.insert_one(self.__dict__)

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})

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
