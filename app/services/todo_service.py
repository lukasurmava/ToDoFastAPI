from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.resources.strings import TITLE_CANT_BE_EMPTY, TODO_NOT_FOUND, TODO_DELETED, NO_TODO_FOR_THIS_USER, TODO_WITH_THIS_USER_NOT_FOUND, TODOS_WITH_THIS_PRIORITY_NOT_FOUND
from app.schemas import TodoCreate, TodoUpdate
from app.database import Todo, PriorityEnum
from app.services.user_service import read_user_by_id
from app.repositories.todo_repository import insert_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo, get_todo_by_user, get_todo_by_priority

def todo_create(todo: TodoCreate, db: Session):
    if not todo.title:
        raise HTTPException(status_code=422, detail=TITLE_CANT_BE_EMPTY)
    if todo.user_id:
        read_user_by_id(todo.user_id, db)
    new_todo = Todo(title=todo.title, description=todo.description, status=todo.status, priority=todo.priority, user_id=todo.user_id)
    return insert_todo(new_todo, db)

def read_all_todos(db: Session):
    return get_all_todos(db)

def read_todo_by_id(todo_id: int, db: Session):
    db_todo = get_todo_by_id(todo_id, db)
    if not db_todo:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return db_todo

def todo_update(todo_id: int, todo: TodoUpdate, db: Session):
    if not todo.title:
        raise HTTPException(status_code=422, detail=TITLE_CANT_BE_EMPTY)
    if todo.user_id:
        read_user_by_id(todo.user_id, db)
    db_todo = read_todo_by_id(todo_id, db)
    return update_todo(db_todo, todo, db)

def todo_delete(todo_id: int, db: Session):
    db_todo = get_todo_by_id(todo_id, db)
    delete_todo(db_todo, db)
    return {"detail": TODO_DELETED}

def read_todo_by_user(user_id: int, db: Session):
    read_user_by_id(user_id, db)
    db_todos = get_todo_by_user(user_id, db)
    if not db_todos:
        raise HTTPException(status_code=404, detail=NO_TODO_FOR_THIS_USER)
    return db_todos

def read_todo_by_todoid_userid(user_id: int, todo_id: int, db: Session):
    read_user_by_id(user_id, db)
    db_todo = read_todo_by_id(todo_id, db)
    if db_todo.user_id != user_id:
        raise HTTPException(status_code=404, detail=TODO_WITH_THIS_USER_NOT_FOUND)
    return db_todo

def read_todo_by_priority(priority: PriorityEnum, db: Session):
    db_todo = get_todo_by_priority(priority,db)
    if not db_todo:
        raise HTTPException(status_code=404, detail=TODOS_WITH_THIS_PRIORITY_NOT_FOUND)
    return db_todo
