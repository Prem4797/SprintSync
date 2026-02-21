from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.core.db import get_session
from app.models.task_manager import Task, User
from app.api.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Link the task to the logged-in user
    task.user_id = current_user.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/", response_model=List[Task])
def read_tasks(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Users see their own tasks; Admins see everything
    if current_user.is_admin:
        return session.exec(select(Task)).all()
    return session.exec(select(Task).where(Task.user_id == current_user.id)).all()