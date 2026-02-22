import time
from fastapi import FastAPI, Request
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import auth, tasks, ai
from app.core.db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="SprintSync",
    description="Lean internal tool for task management and AI planning.",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate latency
    duration = (time.time() - start_time) * 1000
    
    log_dict = {
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "latency": f"{duration:.2f}ms"
    }
    
    logger.info(f"ACCESS LOG: {log_dict}")
    
    return response

# Expose /metrics for Prometheus
Instrumentator().instrument(app).expose(app)

# App routes 
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(ai.router)

@app.get("/")
def read_root():
    return {"status": "SprintSync API is running", "docs": "/docs"}