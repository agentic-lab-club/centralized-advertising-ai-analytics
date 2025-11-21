from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import test_mock, scheduler
from app.services.scheduler import scheduler_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler_service.start()
    yield
    # Shutdown
    scheduler_service.stop()

app = FastAPI(
    title="DEMETRA AI Analytics API",
    description="AI-powered advertising analytics dashboard",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(test_mock.router)
app.include_router(scheduler.router)

@app.get("/")
def read_root():
    return {
        "message": "DEMETRA AI Analytics API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/test-simple")
def test_simple():
    return {"message": "API is working!", "timestamp": "2025-11-22T02:24:00"}
