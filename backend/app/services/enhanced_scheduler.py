from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.configs.database import SessionLocal
from app.services.ml_sync_service import MLSyncService
from app.services.llm_service import LLMService
from app.models.recommendation import Recommendation
from app.models.campaign import Campaign
import logging

logger = logging.getLogger(__name__)

class EnhancedScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
    
    def ml_dashboard_sync(self):
        """30-minute ML dashboard sync task"""
        logger.info("🚀 Starting 30-minute ML dashboard sync...")
        db = SessionLocal()
        
        try:
            # Run ML sync service
            ml_sync = MLSyncService(db)
            ml_sync.run_all()
            
            # Generate LLM recommendations
            llm_service = LLMService()
            
            # Get real analytics data
            total_campaigns = db.query(Campaign).count()
            
            analytics_data = {
                "total_campaigns": total_campaigns,
                "channels": ["facebook", "instagram", "google_ads", "tiktok"],
                "sync_type": "scheduled_30min"
            }
            
            ml_predictions = {
                "roi_forecasts": "updated",
                "timeseries_data": "refreshed",
                "budget_recommendations": "recalculated"
            }
            
            recommendations = llm_service.generate_recommendations(analytics_data, ml_predictions)
            
            # Save recommendations
            rec = Recommendation(
                recommendations=recommendations,
                summary=recommendations.get('summary', 'Scheduled ML dashboard sync completed')
            )
            db.add(rec)
            db.commit()
            
            logger.info("✅ ML dashboard sync completed successfully")
            
        except Exception as e:
            logger.error(f"❌ ML dashboard sync failed: {e}")
            db.rollback()
        finally:
            db.close()
    
    def start(self):
        """Start the enhanced scheduler"""
        if self.is_running:
            return
        
        # Add ML dashboard sync job (every 30 minutes)
        self.scheduler.add_job(
            func=self.ml_dashboard_sync,
            trigger=IntervalTrigger(minutes=30),
            id='ml_dashboard_sync',
            name='ML Dashboard Sync (30min)',
            replace_existing=True
        )
        
        # Run immediately on startup
        self.scheduler.add_job(
            func=self.ml_dashboard_sync,
            id='startup_ml_sync',
            name='Startup ML Sync'
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("🕒 Enhanced scheduler started - ML sync every 30 minutes")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("🛑 Enhanced scheduler stopped")
    
    def get_jobs(self):
        """Get current scheduled jobs"""
        return [
            {
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in self.scheduler.get_jobs()
        ]

# Global scheduler instance
enhanced_scheduler = EnhancedScheduler()
