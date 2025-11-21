from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.sql import func
from app.configs.database import Base

class MLDashboard(Base):
    __tablename__ = "ml_dashboards"
    
    id = Column(Integer, primary_key=True)
    dashboard_type = Column(String(50))  # 'roi_analysis', 'channel_comparison'
    image_data = Column(LargeBinary)  # PNG bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())