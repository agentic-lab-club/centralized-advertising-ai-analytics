from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database_flexible import get_db
from app.services.sync_service import SyncService
from app.services.scheduler import scheduler_service

router = APIRouter(prefix="/api/scheduler", tags=["scheduler"])

@router.get("/status")
def get_scheduler_status():
    """Get scheduler status"""
    return {
        "running": scheduler_service.scheduler.running,
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in scheduler_service.scheduler.get_jobs()
        ]
    }

@router.post("/sync-now")
def trigger_sync_now(db: Session = Depends(get_db)):
    """Manually trigger sync for testing"""
    count = SyncService.sync_campaigns(db)
    return {"message": f"Manual sync completed: {count} new campaigns"}

@router.post("/start")
def start_scheduler():
    """Start the scheduler"""
    scheduler_service.start()
    return {"message": "Scheduler started"}

@router.post("/stop")
def stop_scheduler():
    """Stop the scheduler"""
    scheduler_service.stop()
    return {"message": "Scheduler stopped"}
