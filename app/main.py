from fastapi import FastAPI, HTTPException, Depends
from database import PriorityEnum
from schemas import UserCreate, UserResponse, UserUpdate, TodoResponse, TodoCreate, TodoUpdate
from typing import List
from sqlalchemy.orm import Session
from database import get_db, seed_db, User, Todo
from services.user_service import read_user_by_id, user_create, read_all_users, user_update, user_delete



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
    user_delete(user_id, db)
    return {"detail": "User deleted"}

# Create a new todos
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    if not todo.title:
        raise HTTPException(status_code=422, detail="Title can't be empty!")
    if not db.query(User).filter(User.id == todo.user_id).first():
        raise HTTPException(status_code=404, detail="User by this id is not found!")
    db_todo = Todo(title=todo.title, description=todo.description, status=todo.status, priority=todo.priority, user_id=todo.user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Get all todos
@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# Get a todos by ID
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# Update a todos by ID
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if not todo.title:
        raise HTTPException(status_code=422, detail="title can't be empty!")
    if not db.query(User).filter(User.id == todo.user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.status = todo.status
    db_todo.priority = todo.priority
    db_todo.user_id = todo.user_id
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Delete a todos by ID
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"}

# Get todos by user
@app.get("/todos/todobyuser/{user_id}", response_model=List[TodoResponse])
async def get_todo_by_user(user_id: int, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    if not db.query(Todo).filter(Todo.user_id == user_id).all():
        raise HTTPException(status_code=404, detail="No todo found for this user!")
    return db.query(Todo).filter(Todo.user_id == user_id).all()

@app.get("/todos/{user_id}/todobyuser/{todo_id}", response_model=TodoResponse)
async def get_todo_by_todoid_userid(user_id: int, todo_id: int, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    todo = db.query(Todo).filter(Todo.user_id == user_id, Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.get("/todos/getbypriority/", response_model=List[TodoResponse])
async def get_todo_by_priority(priority: PriorityEnum, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.priority == priority.value).all()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todos with this priority was not found")
    return db_todo