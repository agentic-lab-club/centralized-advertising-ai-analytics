from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from app.configs.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(String(50), unique=True, index=True)
    channel = Column(String(50), index=True)  # facebook, instagram, google_ads, tiktok
    conversion_rate = Column(Float)
    cost = Column(Float)
    roi = Column(Float)
    clicks = Column(Integer)
    impressions = Column(Integer)
    engagement = Column(Integer)
    date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())