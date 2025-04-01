from pydantic import BaseModel


# --- Pydantic Schemas ---
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