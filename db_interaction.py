from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdateStatus


def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session):
    return db.query(Task).all()

def update_task_status(db: Session, task_id: int, status: str):
    task = get_task(db, task_id)
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
    return task