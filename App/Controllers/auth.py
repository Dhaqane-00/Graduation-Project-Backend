from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models.User import User
import os
from bson import ObjectId

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')
    status = data.get('status', 'Active')

    if 'image' in request.files:
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
    else:
        filename = 'default.jpg'

    image_url = f'{current_app.config["BASE_URL"]}/image/{filename}'

    if User.find_by_email(email):
        return jsonify(message="User already exists"), 400

    new_user = User(name, email, password, role, status, image_url)
    new_user.save_to_db()

    token = User.generate_token(email, role, status)

    user_data = {
        "id": str(new_user._id),
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
        "status": new_user.status,
        "image": new_user.image
    }

    return jsonify(message="User registered successfully", user_data=user_data, token=token), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_data = User.find_by_email(email)
    if user_data and User.verify_password(user_data['password'], password):
        token = User.generate_token(email, user_data['role'], user_data['status'])
        image_url = user_data.get('image', f'{current_app.config["BASE_URL"]}/image/default.jpg')

        # Ensure all ObjectId fields are converted to strings
        user_data['id'] = str(user_data['_id'])
        user_data.pop('_id')  # Remove the original ObjectId

        return jsonify(user_data=user_data, token=token,), 200
    else:
        return jsonify(message="Invalid email or password"), 401
