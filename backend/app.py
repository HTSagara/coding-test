from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
users = db['users']


@app.route('/api/users', methods=['GET'])
def get_users():
    user_list = list(users.find())
    for user in user_list:
        user['_id'] = str(user['_id'])
    return jsonify(user_list)


@app.route('/api/users/<id>', methods=['GET'])
def get_user(id):
    user = users.find_one({'_id': ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    data['created_ts'] = datetime.now().timestamp()
    result = users.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201


@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    data['updated_ts'] = datetime.now().timestamp()
    users.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({'message': 'User updated'})


@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    users.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User deleted'})


if __name__ == '__main__':
    app.run(debug=True)
