from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# Simple in-memory token store (MVP only)
# In production use JWT (flask-jwt-extended)
tokens = {}

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    user = User(name=name, email=email)
    user.password_hash = generate_password_hash(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # generate simple token
    token = str(uuid.uuid4())
    tokens[token] = user.id

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    }), 200


# GET CURRENT USER (protected)
@auth_bp.route('/me', methods=['GET'])
def me():
    token = request.headers.get('Authorization')

    if not token or token not in tokens:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = tokens[token]
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user.to_dict()), 200


# LOGOUT
@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')

    if token in tokens:
        del tokens[token]

    return jsonify({"message": "Logged out successfully"}), 200