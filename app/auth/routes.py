# Authentication routes for login and registration 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database.connection import get_db
from .schemas import UserCreate, UserLogin, UserResponse, Token
from . import services

router = APIRouter()

@router.post("/register",response_model=UserResponse)
def register(user:UserCreate,db:Session = Depends(get_db)):
    try:
        return services.register_user(db,user)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except IntegrityError:
        # Safety net if service didn't convert the DB error
        raise HTTPException(status_code=400, detail="Username or email already exists")
    except Exception:
        # Final safety net to avoid leaking internals
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login", response_model=Token)
def login(user:UserLogin,db: Session=Depends(get_db)):
    try:
        return services.login_user(db,user)
    except ValueError as e:
        raise HTTPException(status_code=401,detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")