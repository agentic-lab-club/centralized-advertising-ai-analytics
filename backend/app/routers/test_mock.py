from fastapi import APIRouter
import random
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/test", tags=["Test Mock"])

def generate_mock_campaign_data():
    """Generate mock campaign data"""
    channels = ["Facebook", "Instagram", "Twitter", "Pinterest", "LinkedIn"]
    campaigns = []
    
    for i in range(10):
        campaign = {
            "id": i + 1,
            "name": f"Campaign {i + 1}",
            "channel": random.choice(channels),
            "budget": random.randint(5000, 50000),
            "spent": random.randint(2000, 45000),
            "impressions": random.randint(10000, 500000),
            "clicks": random.randint(100, 5000),
            "conversions": random.randint(10, 200),
            "ctr": round(random.uniform(0.5, 5.0), 2),
            "cpc": round(random.uniform(0.5, 3.0), 2),
            "roi": round(random.uniform(1.2, 4.5), 2),
            "start_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "status": random.choice(["active", "paused", "completed"])
        }
        campaigns.append(campaign)
    
    return campaigns

def generate_mock_analytics_data():
    """Generate mock analytics data"""
    return {
        "total_campaigns": 25,
        "total_budget": 500000,
        "total_spent": 387500,
        "total_impressions": 2500000,
        "total_clicks": 45000,
        "total_conversions": 1250,
        "average_ctr": 1.8,
        "average_cpc": 2.1,
        "average_roi": 3.2,
        "top_channel": "Instagram",
        "performance_by_channel": [
            {"channel": "Instagram", "roi": 4.2, "budget": 120000, "conversions": 380},
            {"channel": "Facebook", "roi": 3.8, "budget": 150000, "conversions": 420},
            {"channel": "Twitter", "roi": 2.9, "budget": 100000, "conversions": 250},
            {"channel": "Pinterest", "roi": 2.1, "budget": 80000, "conversions": 150},
            {"channel": "LinkedIn", "roi": 3.5, "budget": 50000, "conversions": 50}
        ]
    }

@router.get("/mock-data")
async def get_mock_data():
    """Get mock campaign data"""
    return {
        "status": "success",
        "data": generate_mock_campaign_data(),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/mock-all")
@router.post("/mock-all")
async def generate_mock_all():
    """Generate all mock data (campaigns + analytics) - supports both GET and POST"""
    return {
        "status": "success",
        "campaigns": generate_mock_campaign_data(),
        "analytics": generate_mock_analytics_data(),
        "recommendations": {
            "top_performer": "Instagram",
            "worst_performer": "Pinterest", 
            "budget_suggestion": "Reallocate 20% from Pinterest to Instagram",
            "optimization_tips": [
                "Increase Instagram budget by 25%",
                "Optimize Pinterest creative assets",
                "Test new audience segments on Facebook",
                "Improve Twitter engagement rates"
            ]
        },
        "timestamp": datetime.now().isoformat()
    }
