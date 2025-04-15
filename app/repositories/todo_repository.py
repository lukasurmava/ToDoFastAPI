from app.database import User, Todo, PriorityEnum
from sqlalchemy.orm import Session
from app.schemas import TodoUpdate

def insert_todo(todo: Todo, db: Session):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_all_todos(db: Session):
    return db.query(Todo).all()

def get_todo_by_id(todo_id: int, db: Session):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def update_todo(db_todo: Todo, todo: TodoUpdate, db: Session):
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.status = todo.status
    db_todo.priority = todo.priority
    db_todo.user_id = todo.user_id
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db_todo: Todo, db: Session):
    db.delete(db_todo)
    db.commit()

def get_todo_by_user(user_id: int, db: Session):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def get_todo_by_priority(priority: PriorityEnum, db: Session):
    return db.query(Todo).filter(Todo.priority == priority.value).all()