from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.configs.database import SessionLocal
from app.services.ml_dashboard_service import MLDashboardService
import logging

logger = logging.getLogger(__name__)

class MLScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.ml_service = MLDashboardService()
        
    def ml_sync_job(self):
        """Job that runs every 30 minutes to update ML dashboards"""
        try:
            logger.info("Starting ML dashboard sync job...")
            db = SessionLocal()
            
            # Generate all dashboards and update database
            charts = self.ml_service.generate_all_dashboards(db)
            
            logger.info(f"ML dashboard sync completed successfully. Generated charts: {list(charts.keys())}")
            db.close()
            
        except Exception as e:
            logger.error(f"ML dashboard sync job failed: {str(e)}")
            if 'db' in locals():
                db.close()
    
    def start_scheduler(self):
        """Start the scheduler with 30-minute interval"""
        try:
            # Add job to run every 30 minutes
            self.scheduler.add_job(
                func=self.ml_sync_job,
                trigger=IntervalTrigger(minutes=30),
                id='ml_dashboard_sync',
                name='ML Dashboard Sync Job',
                replace_existing=True
            )
            
            # Run once immediately on startup
            self.scheduler.add_job(
                func=self.ml_sync_job,
                trigger='date',
                id='ml_dashboard_initial',
                name='ML Dashboard Initial Run',
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info("ML Scheduler started successfully - running every 30 minutes")
            
        except Exception as e:
            logger.error(f"Failed to start ML scheduler: {str(e)}")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("ML Scheduler stopped")
    
    def run_sync_now(self):
        """Manually trigger ML dashboard sync (hands-on execution)"""
        try:
            logger.info("Manual ML dashboard sync triggered...")
            self.ml_sync_job()
            return {"status": "success", "message": "ML dashboard sync completed manually"}
        except Exception as e:
            logger.error(f"Manual ML dashboard sync failed: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_job_status(self):
        """Get current scheduler job status"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        
        return {
            "scheduler_running": self.scheduler.running,
            "jobs": jobs
        }

# Global scheduler instance
ml_scheduler = MLScheduler()
