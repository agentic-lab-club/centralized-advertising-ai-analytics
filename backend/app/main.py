from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.recommendations import router as recommendations_router
from app.routers.test_mock import router as test_mock_router
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DEMETRA AI Analytics API",
    description="AI-powered advertising analytics dashboard",
    version="2.0.0"
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
app.include_router(recommendations_router)
app.include_router(test_mock_router)

@app.get("/")
def read_root():
    return {
        "message": "DEMETRA AI Analytics API",
        "version": "2.0.0",
        "status": "running",
        "features": "recommendations + mock data enabled",
        "endpoints": [
            "GET /api/recommendations/analytics - AI recommendations",
            "GET /api/recommendations/channels - Channel performance",
            "GET /api/recommendations/budget - Budget allocation",
            "POST /api/recommendations/custom - Custom recommendations",
            "GET /api/test/mock-data - Mock campaign data",
            "POST /api/test/mock-all - All mock data"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-11-22T10:56:52"
    }

@app.get("/api/test")
def test_simple():
    return {
        "message": "DEMETRA API is working!", 
        "status": "ok"
    }
