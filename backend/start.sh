#!/bin/sh

# Check if users collection is empty
python -c '
from pymongo import MongoClient
client = MongoClient("mongodb://mongodb:27017/")
db = client["user_db"]
if db.users.count_documents({}) == 0:
    print("Database empty, running parser")
    import subprocess
    subprocess.run(["python", "parser.py"])
else:
    print("Database already seeded, skipping parser")
'

# Start the Flask app
python app.py