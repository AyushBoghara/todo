from sqlalchemy.orm import Session
from ...models import todo as models
from .schemas import CreateTodo, UpdateTodo

def create_todo(db: Session, todo: CreateTodo, user_id: int):
    new_todo = models.Todos(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=user_id,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def list_todos(db: Session, user_id: int):
    return db.query(models.Todos).filter(models.Todos.user_id == user_id).all()

def get_todo(db: Session, todo_id: int, user_id: int):
    return (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id, models.Todos.user_id == user_id)
        .first()
    )

def update_todo(db: Session, todo_id: int, data: UpdateTodo, user_id: int):
    todo = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id, models.Todos.user_id == user_id)
        .first()
    )
    if not todo:
        return None

    if data.title is not None:
        todo.title = data.title
    if data.description is not None:
        todo.description = data.description
    if data.completed is not None:
        todo.completed = data.completed

    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int, user_id: int) -> bool:
    todo = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id, models.Todos.user_id == user_id)
        .first()
    )
    if not todo:
        return {"message": "Todo not found"}

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
