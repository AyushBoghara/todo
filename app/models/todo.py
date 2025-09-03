# Todo database model

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database.connection import Base
from sqlalchemy.orm import relationship


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    
    owner = relationship("User", back_populates="todos")
