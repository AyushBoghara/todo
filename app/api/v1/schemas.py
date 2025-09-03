from pydantic import BaseModel, ConfigDict
from typing import Optional

class CreateTodo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class UpdateTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    completed: bool

class GetTodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    completed: bool
