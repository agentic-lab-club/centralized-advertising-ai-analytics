from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.configs.database_flexible import get_db
from app.services.sync_service import SyncService
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    """APScheduler service for hourly data sync"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            # Add hourly sync job
            self.scheduler.add_job(
                func=self._sync_campaigns_job,
                trigger=CronTrigger(minute=0),  # Every hour at minute 0
                id='hourly_sync',
                name='Hourly Campaign Sync',
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info("Scheduler started - Hourly sync enabled")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    async def _sync_campaigns_job(self):
        """Background job to sync campaigns"""
        try:
            db = next(get_db())
            count = SyncService.sync_campaigns(db)
            logger.info(f"Hourly sync completed: {count} new campaigns")
        except Exception as e:
            logger.error(f"Hourly sync failed: {e}")
        finally:
            db.close()

# Global scheduler instance
scheduler_service = SchedulerService()
