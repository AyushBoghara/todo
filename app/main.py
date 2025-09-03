# Main FastAPI application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.connection import engine, Base
from .auth import routes as auth_routes
from .api.v1 import todos as todo_routes
from .api.v1 import users as user_routes

from . import models  # Import models to register them with SQLAlchemy

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToDo App with Auth")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register auth routes
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

# Register todo routes
app.include_router(todo_routes.router, prefix="/v1", tags=["todos"])
app.include_router(user_routes.router, prefix="/v1", tags=["users"])
