from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.configs.database import SessionLocal
from app.services.ml_dashboard_service import MLDashboardService
import logging

logger = logging.getLogger(__name__)

def ml_dashboard_sync():
    """Task that runs every 30 minutes to generate ML dashboards"""
    logger.info("🔄 Starting ML dashboard sync...")
    
    db = SessionLocal()
    
    try:
        ml_service = MLDashboardService()
        ml_service.generate_all_dashboards(db)
        logger.info("✅ ML dashboard sync completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Error in ML dashboard sync: {str(e)}")
    
    finally:
        db.close()

def start_ml_scheduler():
    """Start the ML dashboard scheduler"""
    scheduler = BackgroundScheduler()
    
    # Run every 30 minutes
    scheduler.add_job(
        func=ml_dashboard_sync,
        trigger=IntervalTrigger(minutes=30),
        id='ml_dashboard_sync',
        name='ML Dashboard Generation (every 30 min)',
        replace_existing=True
    )
    
    # Run immediately on startup
    scheduler.add_job(
        func=ml_dashboard_sync,
        id='startup_ml_sync',
        name='Startup ML Dashboard Generation',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("🚀 ML Dashboard scheduler started (30-minute intervals)")
    
    return scheduler
