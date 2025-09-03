# User database model

from sqlalchemy import Column,Integer,String
from app.database.connection import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String,unique=True,index=True,nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    todos = relationship("Todos", back_populates="owner")
