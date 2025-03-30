from fastapi import FastAPI, Depends
from sqlalchemy.orm import session
from database import SessionLocal, engine, Base, User
from schemas import UserCreate, UserResponse
from typing import List

# Initialize FastAPI
app = FastAPI()

# Create tables in database (only needed for in-memory DB)
Base.metadata.create_all(bind=engine)

# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_db():
    db_session = SessionLocal()
    users_to_create = [
        {"username": "dorandel", "email": "surmava@gmail.com"},
        {"username": "chuvaldesa", "email": "chuvaldesa@gmail.com"},
        {"username": "liova", "email": "liova@gmail.com"},
    ]
    for user in users_to_create:
        new_seed_user = UserCreate(username=user["username"], email=user["email"])
        db_session.add(new_seed_user)
    db_session.commit()
    db_session.close()

@app.get("/users/create", response_model=UserResponse)
def create_users(user: UserCreate, db: SessionLocal = Depends(get_db)):
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users", response_model=List[UserResponse])
def get_all_users(db: SessionLocal = Depends(get_db)):
    return db.query(User).all()

@app.on_event("startup")
def on_startup():
    seed_db()