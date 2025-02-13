# User Management System

A full-stack web application for managing users with role-based access control. Built with Vue.js 3 for the frontend, Flask for the backend API, and MongoDB for data storage.

## Features

- View, create, edit, and delete users
- Role-based user management
- Timezone preferences for each user
- Responsive data table with sorting and filtering
- Detailed user view with edit capabilities
- Docker containerization for easy deployment

## Tech Stack

- **Frontend**: Vue.js 3 with Vuetify 3 for UI components
- **Backend**: Flask (Python) with RESTful API
- **Database**: MongoDB
- **Containerization**: Docker and Docker Compose

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

```bash
git clone <repository-url>
cd user-management-system
```

2. Start the application using Docker Compose:

```bash
docker-compose up --build
```

This command will:

- Build and start the MongoDB container
- Build and start the Flask backend service
- Build and start the Vue.js frontend service
- Initialize the database with sample user data

3. Access the application:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- MongoDB: localhost:27017

## Data Initialization Scripts

### parser.py

The `parser.py` script is responsible for seeding the MongoDB database with initial user data. Here's how it works:

1. **Data Structure**:

   - Uses Python dataclasses to define the user model structure
   - `UserPreferences` class: Handles user timezone preferences
   - `User` class: Main user data structure containing:
     - username
     - password
     - roles (parsed from boolean flags)
     - preferences
     - timestamps
     - active status

2. **Role Parsing**:

   - Converts boolean flags from JSON into role strings
   - Maps flags to roles:
     - `is_user_admin` → 'admin'
     - `is_user_manager` → 'manager'
     - `is_user_tester` → 'tester'

3. **Data Processing**:
   - Reads from `users.json`
   - Converts ISO format timestamps to Unix timestamps
   - Creates unique MongoDB index on username
   - Handles duplicate user entries gracefully

### start.sh

The `start.sh` script is a shell script that manages the application startup process:

1. **Database Check**:

   ```bash
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
   ```

   - Connects to MongoDB
   - Checks if the users collection is empty
   - Runs parser.py only if no users exist

2. **Application Start**:
   - Executes `python app.py` to start the Flask application
   - Ensures proper initialization sequence

This initialization process ensures that:

- The database is properly seeded on first run
- No duplicate data is created on subsequent runs
- The application starts with required initial data
- The startup process is automated and reliable

## Project Structure

```
.
├── frontend/               # Vue.js frontend application
│   ├── src/               # Source files
│   ├── Dockerfile         # Frontend container configuration
│   └── package.json       # Node.js dependencies
├── backend/               # Flask backend application
│   ├── app.py            # Main application file
│   ├── parser.py         # Database seeding script
│   ├── Dockerfile        # Backend container configuration
│   └── requirements.txt   # Python dependencies
└── docker-compose.yml     # Docker services configuration
```

## API Endpoints

- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get a specific user
- `POST /api/users` - Create a new user
- `PUT /api/users/<id>` - Update a user
- `DELETE /api/users/<id>` - Delete a user
