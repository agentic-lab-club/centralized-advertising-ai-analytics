from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.configs.database import Base

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50))  # 'roi_drop', 'cost_spike', 'low_conversion', 'anomaly'
    severity = Column(String(20))    # 'low', 'medium', 'high', 'critical'
    channel = Column(String(50))
    message = Column(Text)
    metric_value = Column(Float)
    threshold_value = Column(Float)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
