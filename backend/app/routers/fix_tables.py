from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.configs.database import get_db, engine

router = APIRouter(prefix="/api/fix", tags=["Fix"])

@router.post("/create-tables")
async def create_ml_tables():
    """Create ML tables with raw SQL"""
    try:
        with engine.connect() as conn:
            # Create tables
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
            
            # Insert sample data
            conn.execute(text("""
                DELETE FROM ml_roi_forecast;
                INSERT INTO ml_roi_forecast (channel, roi_forecast, confidence_score) VALUES
                ('Facebook', 3.2, 0.85),
                ('Instagram', 2.8, 0.90),
                ('Twitter', 2.5, 0.80),
                ('Pinterest', 1.8, 0.75);
            """))
            
            conn.execute(text("""
                DELETE FROM ml_budget_rec;
                INSERT INTO ml_budget_rec (channel, roi_pred, conversion_pred, acquisition_cost, recommended_budget) VALUES
                ('Facebook', 3.2, 0.08, 7500, 35000),
                ('Instagram', 2.8, 0.09, 7200, 30000),
                ('Twitter', 2.5, 0.07, 8000, 25000),
                ('Pinterest', 1.8, 0.06, 8500, 10000);
            """))
            
            conn.commit()
            
        return {
            "status": "success",
            "message": "ML tables created and populated with sample data",
            "tables": ["ml_roi_forecast", "ml_roi_timeseries", "ml_reach_ctr_timeseries", "ml_budget_rec"]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
