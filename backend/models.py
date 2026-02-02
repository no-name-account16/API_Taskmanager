from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    # Table name in database {users}
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Primary key - unique identifier for each user
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    # Relationship to tasks
    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    # Table name in database {tasks}
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # Primary key - unique identifier for each task
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)  # Task description - optional field, can be null
    status = Column(String, nullable=False)  # Task status 'pending', 'in_progress', 'completed', required field
    due_date = Column(DateTime, nullable=False)  # Due date - when the task should be completed, required field
    # Foreign key - links task to the user who owns it, required field
    # References the 'id' column in the 'users' table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")  # Relationship to user

