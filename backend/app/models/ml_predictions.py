from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from app.configs.database import Base

class MLROIForecast(Base):
    __tablename__ = "ml_roi_forecast"
    
    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(50), index=True)
    roi_forecast = Column(Float)
    confidence_score = Column(Float, default=0.85)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MLROITimeSeries(Base):
    __tablename__ = "ml_roi_timeseries"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    channel = Column(String(50), index=True)
    roi_actual = Column(Float)
    conversion_actual = Column(Float)
    roi_pred = Column(Float)
    conversion_pred = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MLReachCTRTimeSeries(Base):
    __tablename__ = "ml_reach_ctr_timeseries"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    channel = Column(String(50), index=True)
    reach_actual = Column(Integer)
    ctr_actual = Column(Float)
    reach_pred = Column(Integer)
    ctr_pred = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MLBudgetRec(Base):
    __tablename__ = "ml_budget_rec"
    
    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(50), index=True)
    roi_pred = Column(Float)
    conversion_pred = Column(Float)
    acquisition_cost = Column(Float)
    recommended_budget = Column(Float)
    total_budget = Column(Float, default=100000.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
