from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.configs.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True)
    recommendations = Column(JSONB)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())