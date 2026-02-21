import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "SprintSync"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/sprintsync")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key_123")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()