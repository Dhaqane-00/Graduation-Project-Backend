from flask import Blueprint, request, jsonify
from models.User import User
from bson import ObjectId

bp = Blueprint('auth', __name__, url_prefix='/auth')

def convert_objectid_to_str(user_data):
    if '_id' in user_data:
        user_data['_id'] = str(user_data['_id'])
    return user_data

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')  # Default role is 'User'
    status = data.get('status', 'Active')  # Default status is 'Active'

    if User.find_by_email(email):
        return jsonify(message="User already exists"), 400

    new_user = User(name, email, password, role, status)
    new_user.save_to_db()

    token = User.generate_token(email, role, status)

    return jsonify(message="User registered successfully", token=token), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_data = User.find_by_email(email)
    if user_data and User.verify_password(user_data['password'], password):
        token = User.generate_token(email, user_data['role'], user_data['status'])
        user_data = convert_objectid_to_str(user_data)
        return jsonify(user_data=user_data, token=token), 200
    else:
        return jsonify(message="Invalid email or password"), 401
