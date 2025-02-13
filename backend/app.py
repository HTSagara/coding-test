# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from pymongo import MongoClient, errors
from bson import ObjectId
from datetime import datetime
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}},
     supports_credentials=True)


def get_db_client():
    try:
        client = MongoClient(
            'mongodb://mongodb:27017/',
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            retryWrites=True
        )
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")

        # Ensure unique index on username
        db = client['user_db']
        db['users'].create_index([('username', pymongo.ASCENDING)],
                                 unique=True)

        return client
    except errors.ServerSelectionTimeoutError as e:
        logger.error("MongoDB connection timeout: %s", str(e))
        return None
    except Exception as e:
        logger.error(f"An error occurred connecting to MongoDB: {e}")
        return None


# Initialize database connection
client = get_db_client()
db = client['user_db'] if client is not None else None


@app.route('/')
def home():
    if db is None:
        return jsonify({
            "status": "error",
            "message": "Database connection not available"
        }), 500
    return jsonify({
        "status": "ok",
        "message": "API is running",
        "mongodb_status": "connected"
    })


@app.route('/api/users', methods=['GET'])
def get_users():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        users_collection = db['users']
        user_list = list(users_collection.find())

        if not user_list:  # Add empty collection check
            return jsonify([]), 200

        for user in user_list:
            user['_id'] = str(user['_id'])
        return jsonify(user_list)
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/users/<id>', methods=['GET'])
def get_user(id):
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        users_collection = db['users']
        user = users_collection.find_one({'_id': ObjectId(id)})
        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user)
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error retrieving user {id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        users_collection = db['users']
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Check for existing username
        if users_collection.find_one({"username": data.get('username')}):
            return jsonify({"error": "Username already exists"}), 409

        data['created_ts'] = datetime.now().timestamp()
        result = users_collection.insert_one(data)
        # Get the full inserted document
        new_user = users_collection.find_one({'_id': result.inserted_id})
        new_user['_id'] = str(new_user['_id'])  # Convert ObjectId
        return jsonify(new_user), 201  # Return complete user data

    except pymongo.errors.DuplicateKeyError as e:
        logger.error(f"Duplicate insert attempt: {str(e)}")
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        users_collection = db['users']
        data = request.json
        data.pop('_id', None)

        data['updated_ts'] = datetime.now().timestamp()

        # Check if user exists
        existing_user = users_collection.find_one({'_id': ObjectId(id)})
        if not existing_user:
            return jsonify({"error": "User not found"}), 404

        # Proceed with update
        result = users_collection.update_one(
            {
                '_id': ObjectId(id)
            },
            {
                '$set': data
            }
            )
        if result.modified_count:
            return jsonify({'message': 'User updated'})
        return jsonify({'message': 'No changes made'}), 200
    except Exception as e:
        logger.error(f"Error updating user {id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        users_collection = db['users']
        result = users_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({'message': 'User deleted'})
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting user {id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health_check():
    if db is None:
        return jsonify({"status": "unhealthy", "error":
                        "Database connection unavailable"}), 500
    try:
        db.command('ping')
        return jsonify({"status": "healthy"}), 200
    except errors.ServerSelectionTimeoutError:
        logger.error("MongoDB connection failed")
        return jsonify({"status": "unhealthy"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
