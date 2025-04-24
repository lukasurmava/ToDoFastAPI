from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_id, insert_user, get_all_users, update_user, delete_user
from fastapi import HTTPException
from app.resources.strings import USER_NOT_FOUND, USERNAME_CANT_BE_EMPTY, USER_DELETED
from app.schemas import UserCreate, UserUpdate
from app.models import User


def user_create(user: UserCreate, db: Session):
    if not user.username:
        raise HTTPException(status_code=422, detail=USERNAME_CANT_BE_EMPTY)
    new_user = User(username = user.username, email= user.email)
    return insert_user(new_user,db)

def read_all_users(db: Session):
    return get_all_users(db)

def read_user_by_id(user_id: int, db: Session):
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return db_user

def user_update(user_id: int, user: UserUpdate, db: Session):
    if not user.username:
        raise HTTPException(status_code=422, detail=USERNAME_CANT_BE_EMPTY)
    db_user = read_user_by_id(user_id, db)
    return update_user(db_user, user, db)

def user_delete(user_id: int, db: Session):
    db_user = read_user_by_id(user_id, db)
    delete_user(db_user, db)
    return {"detail": USER_DELETED}