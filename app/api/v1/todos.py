# Todo management API endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database.connection import get_db
from ...middleware.auth import get_current_user
from ...models.user import User
from .schemas import CreateTodo, UpdateTodo, TodoOut
from .service import create_todo, list_todos, get_todo, update_todo, delete_todo

router = APIRouter()
# create a data todo
@router.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo_endpoint(todo: CreateTodo, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_todo(db, todo, user_id=current_user.id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# get all data 
@router.get("/todos", response_model=list[TodoOut])
def list_todos_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return list_todos(db, user_id=current_user.id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# get a single data  by id 
@router.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo_endpoint(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        todo = get_todo(db, todo_id, user_id=current_user.id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return todo
# update a data 
@router.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo_endpoint(
    todo_id: int,
    data: UpdateTodo,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = update_todo(db, todo_id, data, user_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# delete a data 
@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_endpoint(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_todo(db, todo_id, user_id=current_user.id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    