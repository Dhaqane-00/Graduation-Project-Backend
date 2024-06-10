from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

class User:
    def __init__(self, name, email, password, role='User', status='Active'):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.status = status

    def save_to_db(self):
        client = MongoClient('localhost', 27017)
        db = client['predictions_db']
        users_collection = db['users']
        user_data = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'status': self.status
        }
        users_collection.insert_one(user_data)

    @staticmethod
    def find_by_email(email):
        client = MongoClient('localhost', 27017)
        db = client['predictions_db']
        users_collection = db['users']
        return users_collection.find_one({'email': email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    @staticmethod
    def generate_token(email, role, status):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=70),
            'iat': datetime.datetime.utcnow(),
            'email': email,
            'role': role,
            'status': status
        }
        return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
