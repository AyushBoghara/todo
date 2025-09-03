# ToDo App (FastAPI + JWT Auth + SQLite)

A production-ready FastAPI backend for managing users and personal ToDo items.
It includes registration, login (JWT), and full CRUD for todos scoped to the authenticated user.

## Features
- Authentication: register and login with JWT access tokens
- Authorization: all ToDo operations are protected and tied to the current user
- Full ToDo CRUD: create, list, get, update, delete
- Users listing endpoint (for debugging/admin use)
- SQLite database via SQLAlchemy ORM
- Pydantic v2 models (from_attributes enabled)
- Auto-reload dev server via run.py

## Quick Start
1) Install dependencies
```bash
pip install -r requirements.txt
```

2) Run the server (recommended)
```bash
python run.py
```
- The app starts at http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs

Alternative commands
```bash
uvicorn run:app --reload
# or
python -m app.main  # basic import check, not the standard run method
```

## Configuration
The project uses sensible defaults in code:
- Database URL: sqlite:///./todo.db (see app/database/connection.py)
- JWT Secret/Algorithm/Expiry: see app/core/security.py (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)

For local development, you can keep defaults.
For production, change SECRET_KEY and database settings in code or refactor to load from environment variables.
(.env.example is included as a reference, but current code does not auto-load .env.)

## Project Structure
```
ToDoApp/
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI app instance and routers
│   ├── auth/
│   │   ├── routes.py                 # /auth/register, /auth/login
│   │   ├── services.py               # Register/Login business logic
│   │   └── schemas.py                # UserCreate, UserLogin, UserResponse, Token
│   ├── core/
│   │   ├── config.py
│   │   └── security.py               # Hash/verify password, JWT create_access_token
│   ├── database/
│   │   └── connection.py             # SQLAlchemy engine, SessionLocal, get_db
│   ├── middleware/
│   │   └── auth.py                   # get_current_user (JWT -> DB user)
│   ├── api/
│   │   └── v1/
│   │       ├── todos.py              # Secured ToDo endpoints
│   │       ├── users.py              # Users listing endpoint
│   │       └── schemas.py            # CreateTodo, UpdateTodo, TodoOut
│   └── models/
│       ├── user.py                   # SQLAlchemy User model
│       └── todo.py                   # SQLAlchemy Todos model
├── run.py                            # Entrypoint to start dev server
├── requirements.txt
└── README.md
```

## Data Models (SQLAlchemy)
- User (app/models/user.py)
  - id, username (unique), email (unique), hashed_password
  - todos relationship to Todos
- Todos (app/models/todo.py)
  - id, title, description, completed, user_id (FK -> Users.id)
  - owner relationship to User

## Pydantic Schemas
- auth/schemas.py
  - UserCreate {username, email, password}
  - UserLogin {email, password}
  - UserResponse {id, username, email}
  - Token {access_token, token_type}
- api/v1/schemas.py
  - CreateTodo {title, description?, completed=false}
  - UpdateTodo {title?, description?, completed?}
  - TodoOut {id, title, description?, completed} with model_config = ConfigDict(from_attributes=True)

## Auth Flow
1) Register
- POST /auth/register with JSON {username, email, password}
- Validates uniqueness on username and email (database unique constraints + pre-checks)
- Returns UserResponse

2) Login
- POST /auth/login with JSON {email, password}
- On success returns Token: {"access_token": "...", "token_type": "bearer"}
- Include Authorization: Bearer <access_token> on all protected routes

JWT Subject
- The token contains sub=email and is validated in middleware/auth.py to fetch the current User from DB.

## API Reference
Base URL: http://127.0.0.1:8000

Auth
- POST /auth/register -> 200 OK (UserResponse)
- POST /auth/login -> 200 OK (Token)

Todos (secured — requires Authorization: Bearer <token>)
- POST /v1/todos -> 201 Created (TodoOut)
- GET  /v1/todos -> 200 OK (list[TodoOut])
- GET  /v1/todos/{todo_id} -> 200 OK (TodoOut) or 404
- PUT  /v1/todos/{todo_id} -> 200 OK (TodoOut) or 404
- DELETE /v1/todos/{todo_id} -> 204 No Content or 404

Legacy alias routes (backward compatibility)
- GET /v1/get_todos -> same as GET /v1/todos
- GET /v1/get_todos/{todo_id} -> same as GET /v1/todos/{todo_id}

Users
- GET /v1/users -> 200 OK (list[UserResponse])
  - Note: this endpoint is currently public; protect it if needed.

## Example Requests (curl)
Register
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"secret"}'
```

Login
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"secret"}' | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
```

Create ToDo
```bash
curl -X POST http://127.0.0.1:8000/v1/todos \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Read docs","description":"FastAPI"}'
```

List ToDos
```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/v1/todos
```

Get One
```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/v1/todos/1
```

Update
```bash
curl -X PUT http://127.0.0.1:8000/v1/todos/1 \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

Delete
```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/v1/todos/1
```

## Testing
Run tests with pytest:
```bash
pytest -q
```

## Troubleshooting
- ModuleNotFoundError: No module named 'ToDoApp'
  - Ensure imports are relative (fixed in app/api/v1/users.py)
- 401 Unauthorized on ToDo routes
  - Provide Authorization: Bearer <access_token> header (login first)
- 404 on /v1/get_todos
  - Legacy routes are now available; ensure server has reloaded
- Pydantic v2 warning about orm_mode
  - Resolved by using ConfigDict(from_attributes=True)

## Roadmap / Ideas
- Add pagination and filtering for /v1/todos
- Add proper environment configuration loading (.env) and secrets management
- Protect /v1/users and add user management endpoints
- Add Alembic migrations
- Add CI and more test coverage

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries or support, please contact:
- **Developer:** Ayush M Boghara
- **Email:** [bogharaayush1124@gmail.com]
- **GitHub:** [AyushBoghara](https://github.com/AyushBoghara)


**© 2024-2025 Morse Code Translator Application | Powered by Modern Technologies**

