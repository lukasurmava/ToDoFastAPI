from enum import IntEnum

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool
import enum

# --- Database Setup ---
DATABASE_URL = "sqlite:///:memory:"  # In-memory DB
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Ensures all sessions share the same connection
    echo=True  # Debug: prints SQL statements
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class StatusEnum(IntEnum):
    IN_PROGRESS = 0
    COMPLETED = 1
    PENDING = 2

class PriorityEnum(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


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
    status = Column(Integer)
    priority = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")


# Create the tables
Base.metadata.create_all(bind=engine)


# Dependency: get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_db():
    db: Session = SessionLocal()
    # Only seed if there are no records
    if not db.query(User).first():
        test_users = [
            User(username="chuva", email="chuva@example.com"),
            User(username="liova", email="liova@example.com"),
            User(username="rezili", email="rezili@example.com"),
        ]
        db.add_all(test_users)
        db.commit()
    if not db.query(Todo).first():
        test_todos = [
            Todo(title="vnaxot aba", description="miidi ra imushave", status=1, priority=1, user_id=1)
        ]
        db.add_all(test_todos)
        db.commit()
    db.close()