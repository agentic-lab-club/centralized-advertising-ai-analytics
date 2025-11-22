from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services.ml_dashboard_service import MLDashboardService

router = APIRouter(prefix="/api/sync", tags=["Sync"])

@router.post("/run-now")
async def run_sync_now(db: Session = Depends(get_db)):
    """Manually trigger ML dashboard sync (hands-on execution)"""
    try:
        ml_service = MLDashboardService()
        charts = ml_service.generate_all_dashboards(db)
        return {
            "status": "success", 
            "message": "ML dashboard sync completed manually",
            "charts": charts
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "note": "Tables will be created automatically"
        }

@router.get("/status")
async def get_sync_status():
    """Get current sync scheduler status"""
    return {
        "scheduler_running": False,
        "scheduler_status": "disabled",
        "message": "Scheduler is disabled. Use POST /api/sync/run-now for manual sync",
        "jobs": []
    }

@router.post("/start-scheduler")
async def start_scheduler():
    """Start the ML dashboard scheduler"""
    return {
        "status": "disabled", 
        "message": "Scheduler is permanently disabled"
    }

@router.post("/stop-scheduler")
async def stop_scheduler():
    """Stop the ML dashboard scheduler"""
    return {
        "status": "disabled", 
        "message": "Scheduler is permanently disabled"
    }

@router.post("/generate-sample-data")
async def generate_sample_data(db: Session = Depends(get_db)):
    """Generate sample ML data for testing"""
    try:
        ml_service = MLDashboardService()
        charts = ml_service.generate_all_dashboards(db)
        return {
            "status": "success", 
            "message": "Sample ML data generated",
            "charts": charts
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "note": "Tables will be created automatically on retry"
        }
