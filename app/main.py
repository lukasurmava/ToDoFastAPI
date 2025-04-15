from fastapi import FastAPI, Depends
from database import PriorityEnum
from schemas import UserCreate, UserResponse, UserUpdate, TodoResponse, TodoCreate, TodoUpdate
from typing import List
from sqlalchemy.orm import Session
from database import get_db, seed_db
from services.user_service import read_user_by_id, user_create, read_all_users, user_update, user_delete
from services.todo_service import todo_create, read_all_todos, read_todo_by_id, todo_update, todo_delete, read_todo_by_user, read_todo_by_todoid_userid, read_todo_by_priority



# --- FastAPI App Setup ---
app = FastAPI()

# Seed the database with test records at startup
@app.on_event("startup")
def on_startup():
    seed_db()

# --- CRUD Endpoints ---

# Create a new user
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_create(user, db)

# Get all users
@app.get("/users/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return read_all_users(db)

# Get a user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return read_user_by_id(user_id,db)

# Update a user by ID
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_update(user_id, user, db)

# Delete a user by ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_delete(user_id, db)

# Create a new todos
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return todo_create(todo,db)

# Get all todos
@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return read_all_todos(db)

# Get a todos by ID
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    return read_todo_by_id(todo_id, db)

# Update a todos by ID
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    return todo_update(todo_id, todo, db)

# Delete a todos by ID
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_delete(todo_id, db)

# Get todos by user
@app.get("/todos/todobyuser/{user_id}", response_model=List[TodoResponse])
async def get_todo_by_user(user_id: int, db: Session = Depends(get_db)):
    return read_todo_by_user(user_id, db)

@app.get("/todos/{user_id}/todobyuser/{todo_id}", response_model=TodoResponse)
async def get_todo_by_todoid_userid(user_id: int, todo_id: int, db: Session = Depends(get_db)):
    return read_todo_by_todoid_userid(user_id, todo_id, db)

@app.get("/todos/getbypriority/", response_model=List[TodoResponse])
async def get_todo_by_priority(priority: PriorityEnum, db: Session = Depends(get_db)):
    return read_todo_by_priority(priority, db)