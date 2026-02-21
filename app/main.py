from fastapi import FastAPI
from app.api import auth
from app.core.db import init_db
from contextlib import asynccontextmanager
from app.api import auth, tasks
from app.api import auth, tasks, ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="SprintSync",
    description="Lean internal tool for task management and AI planning.",
    lifespan=lifespan
)

#app initialization
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(ai.router)

@app.get("/")
def read_root():
    return {"status": "SprintSync API is running", "docs": "/docs"}