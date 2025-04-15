from app.database import User
from sqlalchemy.orm import Session
from app.schemas import UserUpdate


def insert_user(user: User, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db_user: User, user: UserUpdate, db: Session):
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db_user: User, db: Session):
    db.delete(db_user)
    db.commit()
