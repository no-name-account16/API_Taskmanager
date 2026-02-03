from sqlalchemy.orm import Session
from models import Task, User
from schemas import TaskCreate, UserCreate
import authentication


# User operations
def create_user(db: Session, user: UserCreate):
    #  Create a new user
    hashed_password = authentication.get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Task operations
def create_task(db: Session, task: TaskCreate, user_id: int):
    #  Create a new task for a specific user
    db_task = Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int, user_id: int):
    # Get a specific task for a user
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()


def get_tasks(db: Session, user_id: int):
    #  Get all tasks for a user
    return db.query(Task).filter(Task.user_id == user_id).all()


def update_task_status(db: Session, task_id: int, status: str, user_id: int):
    #  Update task status for a user's task
    task = get_task(db, task_id, user_id)
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    #  Delete a user's task
    task = get_task(db, task_id, user_id)
    if task:
        db.delete(task)
        db.commit()
    return task

