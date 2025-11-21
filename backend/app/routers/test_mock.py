from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database_flexible import get_db
from app.services.mock_api import MockAPIService
from app.services.sync_service import SyncService

router = APIRouter(prefix="/api/test", tags=["test"])

@router.get("/mock-data")
def get_mock_data():
    """Get mock data from individual channels"""
    return {
        "facebook": MockAPIService.fetch_facebook_ads(),
        "instagram": MockAPIService.fetch_instagram_ads(),
        "google": MockAPIService.fetch_google_ads(),
        "tiktok": MockAPIService.fetch_tiktok_ads()
    }

@router.get("/mock-all")
def get_all_mock_data():
    """Get combined mock data from all channels"""
    return MockAPIService.fetch_all_channels()

@router.post("/sync-now")
def sync_now(db: Session = Depends(get_db)):
    """Manually trigger sync for testing"""
    count = SyncService.sync_campaigns(db)
    return {"message": f"Sync completed: {count} new campaigns"}
