import os
import logging
from pymongo import MongoClient
import pika

logger = logging.getLogger(__name__)

def get_mongodb_client():
    try:
        client = MongoClient(os.environ.get('MONGODB_URI'))
        logger.info("MongoDB connection established")
        return client
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}", exc_info=True)
        raise

def get_rabbitmq_channel():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ.get('RABBITMQ_URI')))
        channel = connection.channel()
        channel.queue_declare(queue='user_events')
        logger.info("RabbitMQ connection established")
        return channel
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {str(e)}", exc_info=True)
        raise
