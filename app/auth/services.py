# Authentication business logic and services

from sqlalchemy.orm import Session
from ..models.user import User
from .schemas import UserCreate,UserLogin
from ..core.security import hash_password,verify_password,create_access_token
from sqlalchemy.exc import IntegrityError


def register_user(db: Session,user:UserCreate):
    # Check for existing email
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise ValueError("Email already registered")

    # Check for existing username
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise ValueError("Username already taken")

    # hash password in user for security purpose 
    
    hashed_pw =  hash_password(user.password)
    # store data in database 
    db_user = User(username = user.username,email = user.email,hashed_password = hashed_pw)
    # add user 
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Provide a clear validation error message for unique constraint violations
        raise ValueError("Failed to register user due to duplicate username or email") from e
    db.refresh(db_user)
    return db_user


def login_user(db:Session,user:UserLogin):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise ValueError("Invalid credentials")
    
    token = create_access_token({"sub":db_user.email})
    
    return {"access_token":token,"token_type":"bearer"}