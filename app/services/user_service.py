from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_id
from fastapi import HTTPException

def read_user_by_id(user_id: int, db: Session):
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user