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

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_task = session.get(Task, task_id)
    if not db_task or (db_task.user_id != current_user.id and not current_user.is_admin):
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields
    data = task_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_task = session.get(Task, task_id)
    if not db_task or (db_task.user_id != current_user.id and not current_user.is_admin):
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}