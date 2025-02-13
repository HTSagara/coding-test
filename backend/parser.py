# backend/parser.py
from dataclasses import dataclass
import json
from datetime import datetime
import pymongo
from typing import List


@dataclass
class UserPreferences:
    timezone: str


@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    created_ts: float
    active: bool = True


def parse_roles(user_data: dict) -> List[str]:
    roles = []
    role_mappings = {
        'is_user_admin': 'admin',
        'is_user_manager': 'manager',
        'is_user_tester': 'tester'
    }

    for key, role in role_mappings.items():
        if user_data.get(key, False):
            roles.append(role)

    return roles


def parse_user(user_data: dict) -> User:
    # Parse the created_at timestamp
    created_at = datetime.strptime(user_data['created_at'],
                                   '%Y-%m-%dT%H:%M:%SZ')
    created_ts = created_at.timestamp()

    # Create UserPreferences
    preferences = UserPreferences(timezone=user_data['user_timezone'])

    # Create User
    return User(
        username=user_data['user'],
        password=user_data['password'],
        roles=parse_roles(user_data),
        preferences=preferences,
        created_ts=created_ts,
        active=user_data['is_user_active']
    )


def main():
    # MongoDB connection using the service name from docker-compose
    client = pymongo.MongoClient('mongodb://mongodb:27017/')
    db = client['user_db']
    collection = db['users']

    collection.create_index("username", unique=True, background=True)

    # Read JSON file
    with open('users.json', 'r') as file:
        data = json.load(file)

    # Parse and insert users
    for user_data in data['users']:
        user = parse_user(user_data)

        # Convert dataclass to dictionary for MongoDB
        user_dict = {
            'username': user.username,
            'password': user.password,
            'roles': user.roles,
            'preferences': {
                'timezone': user.preferences.timezone
            },
            'active': user.active,
            'created_ts': user.created_ts
        }

        try:
            collection.insert_one(user_dict)
            print(f"Inserted user: {user.username}")
        except pymongo.errors.DuplicateKeyError:
            print(f"Skipped duplicate: {user.username}")


if __name__ == '__main__':
    main()
