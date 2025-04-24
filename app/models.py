from enum import StrEnum
from app.base import Base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool


class StatusEnum(StrEnum):
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    PENDING = "Pending"

class PriorityEnum(StrEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# --- SQLAlchemy Model ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    todos = relationship("Todo", back_populates="user")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")