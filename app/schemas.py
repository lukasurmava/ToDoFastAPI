from pydantic import BaseModel
from app.models import PriorityEnum, StatusEnum

# --- Pydantic Schemas ---

class TodoCreate(BaseModel):
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    user_id: int

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    status: StatusEnum
    priority: PriorityEnum
    user_id: int

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    user_id: int


class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Tells Pydantic to read data from ORM objects