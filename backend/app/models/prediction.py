from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.configs.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(String(50))
    predicted_roi = Column(Float)
    risk_level = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())