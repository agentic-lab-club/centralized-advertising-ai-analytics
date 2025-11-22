from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services.ml_dashboard_service import MLDashboardService
from app.models import MLROIForecast, MLROITimeSeries, MLReachCTRTimeSeries, MLBudgetRec
import os

router = APIRouter(prefix="/api/ml-dashboard", tags=["ML Dashboard"])
ml_service = MLDashboardService()

@router.get("/roi-forecast/chart")
async def get_roi_forecast_chart(db: Session = Depends(get_db)):
    """Get ROI forecast chart as PNG"""
    try:
        chart_path = ml_service.generate_roi_forecast_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        # Return dummy chart on error
        chart_path = ml_service.generate_dummy_chart("ROI Forecast (Error)", "roi_forecast_error.png")
        return FileResponse(chart_path, media_type="image/png")

@router.get("/roi-forecast/data")
async def get_roi_forecast_data(db: Session = Depends(get_db)):
    """Get ROI forecast data as JSON"""
    try:
        forecasts = db.query(MLROIForecast).all()
        return [
            {
                "id": f.id,
                "channel": f.channel,
                "roi_forecast": f.roi_forecast,
                "confidence_score": f.confidence_score,
                "created_at": f.created_at.isoformat()
            }
            for f in forecasts
        ]
    except Exception as e:
        return {"error": "Tables not found", "message": "Run POST /api/sync/generate-sample-data first"}

@router.get("/roi-timeseries/chart")
async def get_roi_timeseries_chart(db: Session = Depends(get_db)):
    """Get ROI timeseries chart as PNG"""
    try:
        chart_path = ml_service.generate_roi_timeseries_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        chart_path = ml_service.generate_dummy_chart("ROI Timeseries (Error)", "roi_timeseries_error.png")
        return FileResponse(chart_path, media_type="image/png")

@router.get("/roi-timeseries/data")
async def get_roi_timeseries_data(db: Session = Depends(get_db)):
    """Get ROI timeseries data as JSON"""
    try:
        timeseries = db.query(MLROITimeSeries).all()
        return [
            {
                "id": t.id,
                "date": t.date.isoformat(),
                "channel": t.channel,
                "roi_actual": t.roi_actual,
                "conversion_actual": t.conversion_actual,
                "roi_pred": t.roi_pred,
                "conversion_pred": t.conversion_pred,
                "created_at": t.created_at.isoformat()
            }
            for t in timeseries
        ]
    except Exception as e:
        return {"error": "Tables not found", "message": "Run POST /api/sync/generate-sample-data first"}

@router.get("/reach-ctr/chart")
async def get_reach_ctr_chart(db: Session = Depends(get_db)):
    """Get reach and CTR chart as PNG"""
    try:
        chart_path = ml_service.generate_reach_ctr_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        chart_path = ml_service.generate_dummy_chart("Reach CTR (Error)", "reach_ctr_error.png")
        return FileResponse(chart_path, media_type="image/png")

@router.get("/reach-ctr/data")
async def get_reach_ctr_data(db: Session = Depends(get_db)):
    """Get reach and CTR data as JSON"""
    try:
        reach_ctr = db.query(MLReachCTRTimeSeries).all()
        return [
            {
                "id": r.id,
                "date": r.date.isoformat(),
                "channel": r.channel,
                "reach_actual": r.reach_actual,
                "ctr_actual": r.ctr_actual,
                "reach_pred": r.reach_pred,
                "ctr_pred": r.ctr_pred,
                "created_at": r.created_at.isoformat()
            }
            for r in reach_ctr
        ]
    except Exception as e:
        return {"error": "Tables not found", "message": "Run POST /api/sync/generate-sample-data first"}

@router.get("/budget-recommendation/chart")
async def get_budget_recommendation_chart(db: Session = Depends(get_db)):
    """Get budget recommendation chart as PNG"""
    try:
        chart_path = ml_service.generate_budget_recommendation_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        chart_path = ml_service.generate_dummy_chart("Budget Rec (Error)", "budget_rec_error.png")
        return FileResponse(chart_path, media_type="image/png")

@router.get("/budget-recommendation/data")
async def get_budget_recommendation_data(db: Session = Depends(get_db)):
    """Get budget recommendation data as JSON"""
    try:
        budget_recs = db.query(MLBudgetRec).all()
        return [
            {
                "id": b.id,
                "channel": b.channel,
                "roi_pred": b.roi_pred,
                "conversion_pred": b.conversion_pred,
                "acquisition_cost": b.acquisition_cost,
                "recommended_budget": b.recommended_budget,
                "created_at": b.created_at.isoformat()
            }
            for b in budget_recs
        ]
    except Exception as e:
        return {"error": "Tables not found", "message": "Run POST /api/sync/generate-sample-data first"}

@router.post("/generate-all")
async def generate_all_dashboards(db: Session = Depends(get_db)):
    """Generate all ML dashboards and update database"""
    try:
        charts = ml_service.generate_all_dashboards(db)
        return {
            "status": "success",
            "message": "All ML dashboards generated successfully",
            "charts": charts
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating dashboards: {str(e)}",
            "solution": "Tables will be created automatically on next request"
        }

@router.get("/status")
async def get_dashboard_status(db: Session = Depends(get_db)):
    """Get status of all ML dashboards"""
    try:
        roi_count = db.query(MLROIForecast).count()
        timeseries_count = db.query(MLROITimeSeries).count()
        reach_ctr_count = db.query(MLReachCTRTimeSeries).count()
        budget_count = db.query(MLBudgetRec).count()
        
        return {
            "status": "ready",
            "roi_forecasts": roi_count,
            "roi_timeseries": timeseries_count,
            "reach_ctr_timeseries": reach_ctr_count,
            "budget_recommendations": budget_count,
            "last_updated": "2024-11-22T04:21:53.626+05:00"
        }
    except Exception as e:
        return {
            "status": "tables_missing",
            "error": str(e),
            "message": "ML tables not found. They will be created automatically when you generate data.",
            "action": "POST /api/sync/generate-sample-data"
        }

router = APIRouter(prefix="/api/ml-dashboard", tags=["ML Dashboard"])
ml_service = MLDashboardService()

@router.get("/roi-forecast/chart")
async def get_roi_forecast_chart(db: Session = Depends(get_db)):
    """Get ROI forecast chart as PNG"""
    try:
        chart_path = ml_service.generate_roi_forecast_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roi-forecast/data")
async def get_roi_forecast_data(db: Session = Depends(get_db)):
    """Get ROI forecast data as JSON"""
    forecasts = db.query(MLROIForecast).all()
    return [
        {
            "id": f.id,
            "channel": f.channel,
            "roi_forecast": f.roi_forecast,
            "confidence_score": f.confidence_score,
            "created_at": f.created_at.isoformat()
        }
        for f in forecasts
    ]

@router.get("/roi-timeseries/chart")
async def get_roi_timeseries_chart(db: Session = Depends(get_db)):
    """Get ROI timeseries chart as PNG"""
    try:
        chart_path = ml_service.generate_roi_timeseries_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roi-timeseries/data")
async def get_roi_timeseries_data(db: Session = Depends(get_db)):
    """Get ROI timeseries data as JSON"""
    timeseries = db.query(MLROITimeSeries).all()
    return [
        {
            "id": t.id,
            "date": t.date.isoformat(),
            "channel": t.channel,
            "roi_actual": t.roi_actual,
            "conversion_actual": t.conversion_actual,
            "roi_pred": t.roi_pred,
            "conversion_pred": t.conversion_pred,
            "created_at": t.created_at.isoformat()
        }
        for t in timeseries
    ]

@router.get("/reach-ctr/chart")
async def get_reach_ctr_chart(db: Session = Depends(get_db)):
    """Get reach and CTR chart as PNG"""
    try:
        chart_path = ml_service.generate_reach_ctr_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reach-ctr/data")
async def get_reach_ctr_data(db: Session = Depends(get_db)):
    """Get reach and CTR data as JSON"""
    reach_ctr = db.query(MLReachCTRTimeSeries).all()
    return [
        {
            "id": r.id,
            "date": r.date.isoformat(),
            "channel": r.channel,
            "reach_actual": r.reach_actual,
            "ctr_actual": r.ctr_actual,
            "reach_pred": r.reach_pred,
            "ctr_pred": r.ctr_pred,
            "created_at": r.created_at.isoformat()
        }
        for r in reach_ctr
    ]

@router.get("/budget-recommendation/chart")
async def get_budget_recommendation_chart(db: Session = Depends(get_db)):
    """Get budget recommendation chart as PNG"""
    try:
        chart_path = ml_service.generate_budget_recommendation_chart(db)
        if os.path.exists(chart_path):
            return FileResponse(chart_path, media_type="image/png")
        raise HTTPException(status_code=404, detail="Chart not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/budget-recommendation/data")
async def get_budget_recommendation_data(db: Session = Depends(get_db)):
    """Get budget recommendation data as JSON"""
    budget_recs = db.query(MLBudgetRec).all()
    return [
        {
            "id": b.id,
            "channel": b.channel,
            "roi_pred": b.roi_pred,
            "conversion_pred": b.conversion_pred,
            "acquisition_cost": b.acquisition_cost,
            "recommended_budget": b.recommended_budget,
            "created_at": b.created_at.isoformat()
        }
        for b in budget_recs
    ]

@router.post("/generate-all")
async def generate_all_dashboards(db: Session = Depends(get_db)):
    """Generate all ML dashboards and update database"""
    try:
        charts = ml_service.generate_all_dashboards(db)
        return {
            "status": "success",
            "message": "All ML dashboards generated successfully",
            "charts": charts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_dashboard_status(db: Session = Depends(get_db)):
    """Get status of all ML dashboards"""
    roi_count = db.query(MLROIForecast).count()
    timeseries_count = db.query(MLROITimeSeries).count()
    reach_ctr_count = db.query(MLReachCTRTimeSeries).count()
    budget_count = db.query(MLBudgetRec).count()
    
    return {
        "roi_forecasts": roi_count,
        "roi_timeseries": timeseries_count,
        "reach_ctr_timeseries": reach_ctr_count,
        "budget_recommendations": budget_count,
        "last_updated": "2024-11-22T03:49:25.859+05:00"
    }
