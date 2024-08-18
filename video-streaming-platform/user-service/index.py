import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient
import pika
import json
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.environ.get('MONGODB_URI'))
db = client.users

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ.get('RABBITMQ_URI')))
channel = connection.channel()
channel.queue_declare(queue='user_events')

@app.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.json
        result = db.users.insert_one(user_data)
        user_id = str(result.inserted_id)
        
        # Publish user registered event
        channel.basic_publish(exchange='',
                              routing_key='user_events',
                              body=json.dumps({'type': 'USER_REGISTERED', 'user_id': user_id}))
        
        logger.info(f"User registered: {user_id}")
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}", exc_info=True)
        return jsonify({"error": "Registration failed"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        login_data = request.json
        user = db.users.find_one({"email": login_data['email'], "password": login_data['password']})
        if user:
            logger.info(f"User logged in: {user['_id']}")
            return jsonify({"message": "Login successful", "user_id": str(user['_id'])}), 200
        else:
            logger.warning(f"Failed login attempt for email: {login_data['email']}")
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        return jsonify({"error": "Login failed"}), 500

if __name__ == '__main__':
    logger.info("User service started")
    app.run(host='0.0.0.0', port=3001)
