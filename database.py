from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import enum

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class Priority(enum.IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class Status(enum.IntEnum):
    IN_PROGRESS = 0
    COMPLETED = 1
    PENDING = 2

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    todos = relationship("Todo", back_populates="user")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")
    priority = Column(Enum(Priority), nullable=False)
    status = Column(Enum(Status), nullable=False)

# Create the table in the database
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def create_new_user(db_session, name: str, email: str):
    new_user = User(username=name, email=email)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

def get_all_users(db_session):
    return db_session.query(User).all()
