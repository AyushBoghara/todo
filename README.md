# ToDo App with Authentication

A FastAPI-based ToDo application with user authentication.

## Features
- User registration and login
- JWT-based authentication
- SQLite database
- RESTful API

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application using one of these methods:

### Method 1: Using the run.py script (Recommended)
```bash
python run.py
```

### Method 2: Using uvicorn directly
```bash
uvicorn run:app --reload
```

### Method 3: Using Python module syntax
```bash
python -m app.main
```

## Fixed Issues
- ✅ Fixed ModuleNotFoundError by using relative imports
- ✅ Added missing `get_db()` dependency function
- ✅ Fixed database query syntax errors
- ✅ Created proper entry point at project root
- ✅ Fixed Pydantic Config class capitalization

## API Endpoints
- POST /auth/register - Register a new user
- POST /auth/login - Login user

## Project Structure
```
ToDoApp/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── auth/
│   │   ├── routes.py        # Authentication endpoints
│   │   ├── services.py      # Business logic
│   │   └── schemas.py       # Pydantic models
│   ├── core/
│   │   ├── config.py
│   │   └── security.py      # JWT & password hashing
│   ├── database/
│   │   └── connection.py    # Database setup
│   └── models/
│       ├── user.py          # User SQLAlchemy model
│       └── todo.py
├── run.py                   # Main entry point
├── requirements.txt
└── README.md
```

## Technologies
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Pydantic
- Uvicorn# todo
