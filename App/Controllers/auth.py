from flask import Blueprint, request, jsonify, current_app, render_template_string
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from Models.User import User
import os
from bson import ObjectId
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

bp = Blueprint('auth', __name__ , url_prefix='/auth')

# Access the environment variables
SECRET_KEY = os.getenv('SECRET_KEY')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.form
    name = data.get('name')
    email = data.get('email').lower()
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
    email = data.get('email').lower()
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
    
@bp.route('/update/<user_id>', methods=['PUT'])
def update(user_id):
    data = request.form
    name = data.get('name')
    email = data.get('email').lower()
    password = data.get('password')
    role = data.get('role')
    status = data.get('status')

    user_data = User.find_by_id(ObjectId(user_id))
    if not user_data:
        return jsonify(message="User not found"), 404

    # Create a User instance and set the attributes manually
    user = User(
        name=user_data.get('name'),
        email=user_data.get('email'),
        password=user_data.get('password'),
        role=user_data.get('role', 'User'),
        status=user_data.get('status', 'Active'),
        image=user_data.get('image', 'default.jpg')
    )
    user._id = user_data['_id']  # Manually set the _id attribute

    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.password = generate_password_hash(password)
    if role:
        user.role = role
    if status:
        user.status = status

    if 'image' in request.files:
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        user.image = f'{current_app.config["BASE_URL"]}/image/{filename}'

    user.update_in_db()  # Save the updated user data

    user_data = {
        "id": str(user._id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "image": user.image
    }

    return jsonify(message="User updated successfully", user_data=user_data), 200

@bp.route('/delete/<user_id>', methods=['DELETE'])
def delete(user_id):
    user_data = User.find_by_id(ObjectId(user_id))
    if not user_data:
        return jsonify(message="User not found"), 404

    User.delete_by_id(ObjectId(user_id))

    return jsonify(message="User deleted successfully"), 200


serializer = URLSafeTimedSerializer(SECRET_KEY)
mail = Mail(current_app)

@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email').lower()

    user_data = User.find_by_email(email)
    if user_data is None:
        return jsonify(message="User not found"), 404

    user = User(**user_data)  # Create a User instance from user data
    token = user.generate_reset_token()
    reset_url = f"{current_app.config['RESET_URL']}?token={token}"

    try:
        msg = Message("Reset Your Password", recipients=[email])
        msg.body = f"Click the link below to reset your password:\n{reset_url}"
        mail.send(msg)
        return jsonify(message="Password reset email sent successfully"), 200
    except Exception as e:
        return jsonify(message="Error sending email"), 500



@bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    password = data.get('password')

    email = User.verify_reset_token(token)
    if email is None:
        return jsonify(message="Invalid or expired token"), 400

    user = User.find_by_email(email)
    if user is None:
        return jsonify(message="User not found"), 404

    User.reset_password(email, password)

    return jsonify(message="Password reset successfully"), 200

