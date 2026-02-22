from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.task_manager import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_data: User, session: Session = Depends(get_session)):
    user_data.id = None
    user_data.hashed_password = hash_password(user_data.hashed_password)
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return {"status": "success", "username": user_data.username}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Standard OAuth2/JWT token issuance 
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token({"sub": user.username}), "token_type": "bearer"}