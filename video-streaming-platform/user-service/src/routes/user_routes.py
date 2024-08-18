from flask import Blueprint, request, jsonify
from controllers.user_controller import register_user, login_user
import logging

logger = logging.getLogger(__name__)

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    logger.info("Received registration request")
    return register_user(request.json)

@user_routes.route('/login', methods=['POST'])
def login():
    logger.info("Received login request")
    return login_user(request.json)
