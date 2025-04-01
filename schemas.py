from pydantic import BaseModel
from database import PriorityEnum, StatusEnum

# --- Pydantic Schemas ---

class TodoCreate(BaseModel):
    title: str
    description: str
    status: int
    priority: int
    user_id: int

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    status: int = None
    priority: int = None
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
        orm_mode = True  # Tells Pydantic to read data from ORM objects