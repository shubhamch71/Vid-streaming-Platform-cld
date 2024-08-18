from models.user_model import User
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def register_user(user_data):
    try:
        user = User.create(user_data)
        logger.info(f"User registered successfully: {user.id}")
        return jsonify({"message": "User registered successfully", "user_id": str(user.id)}), 201
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}", exc_info=True)
        return jsonify({"error": "Registration failed"}), 500

def login_user(login_data):
    try:
        user = User.authenticate(login_data['email'], login_data['password'])
        if user:
            logger.info(f"User logged in successfully: {user.id}")
            return jsonify({"message": "Login successful", "user_id": str(user.id)}), 200
        else:
            logger.warning(f"Failed login attempt for email: {login_data['email']}")
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        return jsonify({"error": "Login failed"}), 500
