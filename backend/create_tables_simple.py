#!/usr/bin/env python3
"""
Simple script to create ML tables
"""
import os
import sys
sys.path.append('/mnt/d/Hackathons/MEITU-university-advertisement_compaign_centralized_ai_system/centralized-advertising-ai-analytics/backend')

from app.configs.database import engine, SessionLocal
from app.models.ml_predictions import MLROIForecast, MLROITimeSeries, MLReachCTRTimeSeries, MLBudgetRec
from sqlalchemy import text
from datetime import date

def create_tables():
    """Create all ML tables"""
    try:
        # Create tables using raw SQL
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ml_roi_forecast (
                    id SERIAL PRIMARY KEY,
                    channel VARCHAR(50),
                    roi_forecast FLOAT,
                    confidence_score FLOAT DEFAULT 0.85,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """))
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ml_roi_timeseries (
                    id SERIAL PRIMARY KEY,
                    date DATE,
                    channel VARCHAR(50),
                    roi_actual FLOAT,
                    conversion_actual FLOAT,
                    roi_pred FLOAT,
                    conversion_pred FLOAT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """))
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ml_reach_ctr_timeseries (
                    id SERIAL PRIMARY KEY,
                    date DATE,
                    channel VARCHAR(50),
                    reach_actual INTEGER,
                    ctr_actual FLOAT,
                    reach_pred INTEGER,
                    ctr_pred FLOAT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """))
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ml_budget_rec (
                    id SERIAL PRIMARY KEY,
                    channel VARCHAR(50),
                    roi_pred FLOAT,
                    conversion_pred FLOAT,
                    acquisition_cost FLOAT,
                    recommended_budget FLOAT,
                    total_budget FLOAT DEFAULT 100000.0,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """))
            
            conn.commit()
            print("✅ ML tables created successfully!")
            
            # Insert sample data
            conn.execute(text("""
                INSERT INTO ml_roi_forecast (channel, roi_forecast, confidence_score) VALUES
                ('Facebook', 3.2, 0.85),
                ('Instagram', 2.8, 0.90),
                ('Twitter', 2.5, 0.80),
                ('Pinterest', 1.8, 0.75)
                ON CONFLICT DO NOTHING;
            """))
            
            conn.execute(text("""
                INSERT INTO ml_budget_rec (channel, roi_pred, conversion_pred, acquisition_cost, recommended_budget) VALUES
                ('Facebook', 3.2, 0.08, 7500, 35000),
                ('Instagram', 2.8, 0.09, 7200, 30000),
                ('Twitter', 2.5, 0.07, 8000, 25000),
                ('Pinterest', 1.8, 0.06, 8500, 10000)
                ON CONFLICT DO NOTHING;
            """))
            
            conn.commit()
            print("✅ Sample data inserted!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_tables()
