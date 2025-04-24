from enum import StrEnum

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool
from app.models import User, Todo
from app.base import Base


# --- Database Setup ---
DATABASE_URL = "sqlite:///:memory:"  # In-memory DB
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Ensures all sessions share the same connection
    echo=True  # Debug: prints SQL statements
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base = declarative_base()


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
    #from app.models import User, Todo
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
            Todo(title="ბევრი იმუშაოს", description="ჩუვამ ბევრი უნდა იმუშაოს რო ძმა ბიჭებს წყნარად ეძინოთ ღამე", status="In progress", priority="High", user_id=1),
            Todo(title="ლუდები სვას გასკდომამდე", description="ბევრი ლუდი უნდა დალიოს რო მძღნერ ხასიათზე არ იყოს", status="Pending", priority="Medium", user_id=1),
            Todo(title="ლიოვას მელანქოლია", description="უნდა ინერვიულოს, ოჯახში ყველას სანერვიულო ლიოვამ უნდა ინერვიულოს",status="Completed", priority="Low", user_id=2),
            Todo(title="გინებას გადაეჩვიოს", description="გინებას დაეჩვია ბოლო პერიოდი, ვინ იქნება შემდეგი მსხვერპლი არ ვიცით", status="Completed", priority="Low", user_id=2),
            Todo(title="ბინა გაარემონტოს", description="დროა აწი მორჩეს მაგ ბინის რემონტს", status="In progress", priority="Medium", user_id=3),
            Todo(title="დოტკის ლიგა მოხოდოს", description="დიდი გეგმები აქვს რეზილს კიბერსპორტში", status="Pending", priority="High", user_id=3)
        ]
        db.add_all(test_todos)
        db.commit()
    db.close()