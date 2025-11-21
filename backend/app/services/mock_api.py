from faker import Faker
import random
from datetime import datetime, timedelta
from typing import List, Dict

fake = Faker()

class MockAPIService:
    """Simulates real API responses from ad platforms"""
    
    CHANNELS = ['facebook', 'instagram', 'google_ads', 'tiktok']
    
    @staticmethod
    def fetch_facebook_ads() -> List[Dict]:
        """Mock Facebook Ads API response"""
        campaigns = []
        for _ in range(random.randint(3, 8)):
            campaigns.append({
                'campaign_id': f'FB_{fake.uuid4()[:8]}',
                'channel': 'facebook',
                'conversion_rate': round(random.uniform(0.01, 0.20), 3),
                'cost': round(random.uniform(100, 800), 2),
                'roi': round(random.uniform(0.5, 8.0), 2),
                'clicks': random.randint(100, 5000),
                'impressions': random.randint(1000, 50000),
                'engagement': random.randint(50, 1000),
                'date': (datetime.now() - timedelta(days=random.randint(0, 7))).date()
            })
        return campaigns
    
    @staticmethod
    def fetch_instagram_ads() -> List[Dict]:
        """Mock Instagram Ads API response"""
        campaigns = []
        for _ in range(random.randint(3, 8)):
            campaigns.append({
                'campaign_id': f'IG_{fake.uuid4()[:8]}',
                'channel': 'instagram',
                'conversion_rate': round(random.uniform(0.01, 0.20), 3),
                'cost': round(random.uniform(100, 800), 2),
                'roi': round(random.uniform(0.5, 8.0), 2),
                'clicks': random.randint(100, 5000),
                'impressions': random.randint(1000, 50000),
                'engagement': random.randint(50, 1000),
                'date': (datetime.now() - timedelta(days=random.randint(0, 7))).date()
            })
        return campaigns
    
    @staticmethod
    def fetch_google_ads() -> List[Dict]:
        """Mock Google Ads API response"""
        campaigns = []
        for _ in range(random.randint(3, 8)):
            campaigns.append({
                'campaign_id': f'GA_{fake.uuid4()[:8]}',
                'channel': 'google_ads',
                'conversion_rate': round(random.uniform(0.01, 0.20), 3),
                'cost': round(random.uniform(100, 800), 2),
                'roi': round(random.uniform(0.5, 8.0), 2),
                'clicks': random.randint(100, 5000),
                'impressions': random.randint(1000, 50000),
                'engagement': random.randint(50, 1000),
                'date': (datetime.now() - timedelta(days=random.randint(0, 7))).date()
            })
        return campaigns
    
    @staticmethod
    def fetch_tiktok_ads() -> List[Dict]:
        """Mock TikTok Ads API response"""
        campaigns = []
        for _ in range(random.randint(3, 8)):
            campaigns.append({
                'campaign_id': f'TT_{fake.uuid4()[:8]}',
                'channel': 'tiktok',
                'conversion_rate': round(random.uniform(0.01, 0.20), 3),
                'cost': round(random.uniform(100, 800), 2),
                'roi': round(random.uniform(0.5, 8.0), 2),
                'clicks': random.randint(100, 5000),
                'impressions': random.randint(1000, 50000),
                'engagement': random.randint(50, 1000),
                'date': (datetime.now() - timedelta(days=random.randint(0, 7))).date()
            })
        return campaigns
    
    @classmethod
    def fetch_all_channels(cls) -> List[Dict]:
        """Fetch data from all channels"""
        all_campaigns = []
        all_campaigns.extend(cls.fetch_facebook_ads())
        all_campaigns.extend(cls.fetch_instagram_ads())
        all_campaigns.extend(cls.fetch_google_ads())
        all_campaigns.extend(cls.fetch_tiktok_ads())
        return all_campaigns
