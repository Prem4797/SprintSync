from google import genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_task_suggestion(title: str, use_stub: bool = False):
    """
    Fulfills Requirement: /ai/suggest implements draft task description.
    Updated to Gemini 3 Flash via the modern google-genai SDK.
    """
    if use_stub or not settings.GEMINI_API_KEY:
        return f"STUB: Professional approach for {title}."

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"Provide a concise professional 2-sentence task description for: {title}"
        )
        
        return response.text.strip()
    
    except Exception as e:
        logger.error(f"AI Service Error: {str(e)}")
        return f"AI Error: {str(e)}"