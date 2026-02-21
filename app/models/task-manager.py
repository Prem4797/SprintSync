from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_admin: bool = Field(default=False)
    
    tasks: List["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False) 
    description: Optional[str] = None
    status: str = Field(default="To Do") 
    total_minutes: int = Field(default=0)
    
    user_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="tasks")