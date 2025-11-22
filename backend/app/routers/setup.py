from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.configs.database import get_db, engine

router = APIRouter(prefix="/api/setup", tags=["setup"])

@router.post("/create-ml-tables")
def create_ml_tables(db: Session = Depends(get_db)):
    """Create ML prediction tables if they don't exist"""
    
    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS ml_roi_forecast (
            id SERIAL PRIMARY KEY,
            channel VARCHAR(50),
            roi_forecast FLOAT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        """
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
        """,
        """
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
        """,
        """
        CREATE TABLE IF NOT EXISTS ml_budget_rec (
            id SERIAL PRIMARY KEY,
            channel VARCHAR(50),
            roi_pred FLOAT,
            conversion_pred FLOAT,
            acquisition_cost FLOAT,
            recommended_budget FLOAT,
            total_budget FLOAT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
    ]
    
    try:
        for sql in sql_commands:
            db.execute(text(sql))
        db.commit()
        
        # Verify tables exist
        result = db.execute(text("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name LIKE 'ml_%'
        """))
        tables = [row[0] for row in result.fetchall()]
        
        return {
            "status": "success",
            "message": "ML tables created successfully",
            "tables_created": tables
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to create ML tables: {str(e)}"
        }

@router.get("/check-tables")
def check_tables(db: Session = Depends(get_db)):
    """Check if ML tables exist"""
    try:
        result = db.execute(text("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name LIKE 'ml_%'
        """))
        tables = [row[0] for row in result.fetchall()]
        
        return {
            "status": "success",
            "ml_tables": tables,
            "tables_exist": len(tables) == 4
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
