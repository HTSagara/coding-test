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
