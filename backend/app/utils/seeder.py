import os
import sys
from datetime import datetime, timedelta
from faker import Faker
import random

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.configs.database import SessionLocal, engine, Base
from app.models.campaign import Campaign
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation
from app.models.alert import Alert

fake = Faker()

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def seed_campaigns(db: Session, count: int = 50):
    """Seed campaigns with realistic advertising data"""
    channels = ['facebook', 'instagram', 'google_ads', 'tiktok', 'youtube', 'linkedin']
    
    campaigns = []
    for i in range(count):
        channel = random.choice(channels)
        
        # Generate realistic metrics based on channel
        if channel in ['facebook', 'instagram']:
            base_roi = random.uniform(1.5, 4.0)
            base_conversion = random.uniform(0.02, 0.15)
            base_cost = random.uniform(150, 600)
        elif channel == 'google_ads':
            base_roi = random.uniform(2.0, 6.0)
            base_conversion = random.uniform(0.03, 0.20)
            base_cost = random.uniform(200, 800)
        elif channel == 'tiktok':
            base_roi = random.uniform(1.0, 3.5)
            base_conversion = random.uniform(0.01, 0.12)
            base_cost = random.uniform(100, 500)
        else:  # youtube, linkedin
            base_roi = random.uniform(1.2, 3.8)
            base_conversion = random.uniform(0.02, 0.14)
            base_cost = random.uniform(180, 650)
        
        impressions = random.randint(1000, 50000)
        clicks = int(impressions * random.uniform(0.01, 0.08))  # CTR 1-8%
        engagement = random.randint(50, min(clicks * 2, 2000))
        
        campaign = Campaign(
            campaign_id=f"{channel.upper()}_{fake.uuid4()[:8]}",
            channel=channel,
            conversion_rate=round(base_conversion, 4),
            cost=round(base_cost, 2),
            roi=round(base_roi, 2),
            clicks=clicks,
            impressions=impressions,
            engagement=engagement,
            date=(datetime.now() - timedelta(days=random.randint(0, 30))).date()
        )
        campaigns.append(campaign)
    
    db.add_all(campaigns)
    db.commit()
    print(f"✅ Seeded {count} campaigns!")
    return campaigns

def seed_predictions(db: Session, campaigns):
    """Seed ML predictions for campaigns"""
    predictions = []
    
    for campaign in campaigns[:20]:  # Predict for first 20 campaigns
        # Mock ML prediction logic
        current_roi = campaign.roi
        predicted_roi = current_roi * random.uniform(0.9, 1.3)  # ±30% variation
        
        if predicted_roi < 1.0:
            risk_level = 'high'
        elif predicted_roi < 2.0:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        prediction = Prediction(
            campaign_id=campaign.campaign_id,
            predicted_roi=round(predicted_roi, 2),
            risk_level=risk_level
        )
        predictions.append(prediction)
    
    db.add_all(predictions)
    db.commit()
    print(f"✅ Seeded {len(predictions)} ML predictions!")

def seed_recommendations(db: Session):
    """Seed LLM recommendations"""
    recommendations_data = {
        "channel_comparison": {
            "top_performer": "google_ads",
            "worst_performer": "tiktok",
            "analysis": "Google Ads shows 35% higher ROI than average. TikTok needs creative optimization."
        },
        "budget_allocation": {
            "google_ads": "40%",
            "facebook": "25%",
            "instagram": "20%",
            "tiktok": "10%",
            "others": "5%"
        },
        "optimization_tips": [
            "Increase Google Ads budget by 20%",
            "A/B test TikTok creative formats",
            "Focus on high-converting Facebook audiences",
            "Optimize Instagram Stories placement"
        ]
    }
    
    summary = "Overall campaign performance is strong with 2.8x average ROI. Google Ads leading with 4.2x ROI. Recommend budget reallocation to top-performing channels and creative optimization for underperformers."
    
    recommendation = Recommendation(
        recommendations=recommendations_data,
        summary=summary
    )
    
    db.add(recommendation)
    db.commit()
    print("✅ Seeded LLM recommendations!")

def seed_alerts(db: Session, campaigns):
    """Seed sample alerts"""
    alerts = []
    
    # Find campaigns with issues for realistic alerts
    low_roi_campaigns = [c for c in campaigns if c.roi < 1.5]
    high_cost_campaigns = [c for c in campaigns if c.cost > 500]
    low_conversion_campaigns = [c for c in campaigns if c.conversion_rate < 0.03]
    
    # ROI drop alerts
    for campaign in low_roi_campaigns[:3]:
        alert = Alert(
            alert_type='roi_drop',
            severity='high',
            channel=campaign.channel,
            message=f"ROI dropped to {campaign.roi} for {campaign.channel} campaign {campaign.campaign_id}",
            metric_value=campaign.roi,
            threshold_value=1.5,
            is_read=False
        )
        alerts.append(alert)
    
    # Cost spike alerts
    for campaign in high_cost_campaigns[:2]:
        alert = Alert(
            alert_type='cost_spike',
            severity='medium',
            channel=campaign.channel,
            message=f"Acquisition cost spiked to ${campaign.cost} for {campaign.channel}",
            metric_value=campaign.cost,
            threshold_value=500.0,
            is_read=False
        )
        alerts.append(alert)
    
    # Low conversion alerts
    for campaign in low_conversion_campaigns[:2]:
        alert = Alert(
            alert_type='low_conversion',
            severity='medium',
            channel=campaign.channel,
            message=f"Low conversion rate {campaign.conversion_rate:.2%} for {campaign.channel}",
            metric_value=campaign.conversion_rate,
            threshold_value=0.03,
            is_read=False
        )
        alerts.append(alert)
    
    db.add_all(alerts)
    db.commit()
    print(f"✅ Seeded {len(alerts)} alerts!")

def seed_all():
    """Seed all data for MVP"""
    print("🚀 Starting database seeding for DEMETRA AI Analytics MVP...")
    
    # Create tables first
    create_tables()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data (for development)
        db.query(Alert).delete()
        db.query(Recommendation).delete()
        db.query(Prediction).delete()
        db.query(Campaign).delete()
        db.commit()
        print("🧹 Cleared existing data")
        
        # Seed campaigns
        campaigns = seed_campaigns(db, count=50)
        
        # Seed predictions
        seed_predictions(db, campaigns)
        
        # Seed recommendations
        seed_recommendations(db)
        
        # Seed alerts
        seed_alerts(db, campaigns)
        
        print("🎉 Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   • {db.query(Campaign).count()} campaigns")
        print(f"   • {db.query(Prediction).count()} ML predictions")
        print(f"   • {db.query(Recommendation).count()} LLM recommendations")
        print(f"   • {db.query(Alert).count()} alerts")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_all()
