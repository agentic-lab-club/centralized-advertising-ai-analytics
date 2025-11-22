from fastapi import APIRouter
from app.services.recommendations_service import (
    get_llm_analytics_hf,
    get_channel_data,
    get_budget_recommendations,
    get_hardcoded_recommendations
)
import json

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/analytics")
async def get_analytics_recommendations():
    """Get AI-powered analytics recommendations"""
    try:
        recommendations = get_llm_analytics_hf()
        return json.loads(recommendations)
    except Exception as e:
        return {"error": str(e), "fallback": get_hardcoded_recommendations()}

@router.get("/channels")
async def get_channel_performance():
    """Get channel performance data"""
    return get_channel_data()

@router.get("/budget")
async def get_budget_allocation():
    """Get budget allocation recommendations"""
    return get_budget_recommendations()

@router.post("/custom")
async def get_custom_recommendations(user_data: dict):
    """Get custom recommendations based on user data"""
    try:
        user_prompt = json.dumps(user_data)
        recommendations = get_llm_analytics_hf(user_prompt)
        return json.loads(recommendations)
    except Exception as e:
        return {"error": str(e), "fallback": get_hardcoded_recommendations()}
