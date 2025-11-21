from sqlalchemy.orm import Session
from app.models.campaign import Campaign
from app.services.mock_api import MockAPIService
from typing import List, Dict

class SyncService:
    """Syncs data from mock APIs to database"""
    
    @staticmethod
    def sync_campaigns(db: Session) -> int:
        """Fetch from mock APIs and save to DB"""
        # Fetch from all channels
        campaigns_data = MockAPIService.fetch_all_channels()
        
        count = 0
        for data in campaigns_data:
            # Check if campaign already exists
            existing = db.query(Campaign).filter(
                Campaign.campaign_id == data['campaign_id']
            ).first()
            
            if not existing:
                # Create new campaign
                campaign = Campaign(**data)
                db.add(campaign)
                count += 1
        
        db.commit()
        return count
