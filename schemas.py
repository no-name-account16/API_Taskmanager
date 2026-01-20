from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict


class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum
    due_date: datetime


class TaskCreate(TaskBase):
    pass


class TaskUpdateStatus(BaseModel):
    status: StatusEnum


class Task(TaskBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
