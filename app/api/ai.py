from fastapi import APIRouter, Depends
from app.services.ai_service import get_task_suggestion
from app.api.deps import get_current_user
from app.models.task_manager import User
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI Assist"])

@router.get("/suggest")
def suggest_description(
    title: str, 
    stub: bool = False, 
    current_user: User = Depends(get_current_user)
):
    """
    Takes a short title and returns a professional draft description.
    """
    suggestion = get_task_suggestion(title, use_stub=stub)
    return {
        "title": title,
        "suggested_description": suggestion,
        "mode": "stub" if stub or not settings.GEMINI_API_KEY else "live"
    }