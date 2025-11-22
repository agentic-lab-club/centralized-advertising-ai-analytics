from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.recommendations import router as recommendations_router
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

@app.get("/")
def read_root():
    return {
        "message": "DEMETRA AI Analytics API",
        "version": "2.0.0",
        "status": "running",
        "features": "recommendations enabled",
        "endpoints": [
            "GET /api/recommendations/analytics - AI recommendations",
            "GET /api/recommendations/channels - Channel performance",
            "GET /api/recommendations/budget - Budget allocation",
            "POST /api/recommendations/custom - Custom recommendations"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-11-22T10:24:39"
    }

@app.get("/api/test")
def test_simple():
    return {
        "message": "DEMETRA API is working!", 
        "status": "ok"
    }
