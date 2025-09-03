# User management API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database.connection import get_db
from ...models.user import User
from ...auth.schemas import UserResponse

router = APIRouter()

@router.get("/users", response_model=list[UserResponse])
def list_users_endpoint(db: Session = Depends(get_db)):
    try:
        return db.query(User).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")