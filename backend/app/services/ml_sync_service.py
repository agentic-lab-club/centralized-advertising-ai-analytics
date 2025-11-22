import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Dict, List

from app.models.campaign import Campaign
from app.models.ml_roi_forecast import MLROIForecast
from app.models.ml_roi_timeseries import MLROITimeSeries
from app.models.ml_reach_ctr_timeseries import MLReachCTRTimeSeries
from app.models.ml_budget_rec import MLBudgetRec
from app.models.ml_dashboard import MLDashboard

class MLSyncService:
    def __init__(self, db: Session):
        self.db = db
        self.output_dir = "/tmp/ml_dashboards"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style for consistent charts
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def run_all(self):
        """Run complete ML sync: predictions + chart generation"""
        print("🚀 Starting ML Dashboard Sync...")
        
        # Clear old data
        self._clear_old_predictions()
        
        # Generate new predictions and charts
        self._generate_roi_forecast()
        self._generate_roi_timeseries()
        self._generate_reach_ctr_timeseries()
        self._generate_budget_recommendations()
        
        print("✅ ML Dashboard Sync Complete!")
    
    def _clear_old_predictions(self):
        """Clear old prediction data"""
        self.db.query(MLROIForecast).delete()
        self.db.query(MLROITimeSeries).delete()
        self.db.query(MLReachCTRTimeSeries).delete()
        self.db.query(MLBudgetRec).delete()
        self.db.commit()
    
    def _generate_roi_forecast(self):
        """Generate ROI forecast by channel"""
        # Get campaign data
        campaigns = self.db.query(Campaign).all()
        df = pd.DataFrame([{
            'channel': c.channel,
            'roi': c.roi,
            'conversion_rate': c.conversion_rate,
            'cost': c.cost
        } for c in campaigns])
        
        # Generate forecasts by channel
        forecasts = []
        for channel in df['channel'].unique():
            channel_data = df[df['channel'] == channel]
            
            # Simple forecast: mean + trend
            roi_forecast = channel_data['roi'].mean() * np.random.uniform(1.05, 1.25)
            confidence = np.random.uniform(0.7, 0.95)
            
            forecast = MLROIForecast(
                channel=channel,
                roi_forecast=round(roi_forecast, 2),
                confidence_score=round(confidence, 2)
            )
            forecasts.append(forecast)
        
        self.db.add_all(forecasts)
        self.db.commit()
        
        # Generate chart
        self._create_roi_forecast_chart(forecasts)
    
    def _generate_roi_timeseries(self):
        """Generate ROI and conversion timeseries"""
        campaigns = self.db.query(Campaign).all()
        
        # Create time series data
        timeseries = []
        for i in range(30):  # Last 30 days
            date = datetime.now().date() - timedelta(days=i)
            
            for channel in ['facebook', 'instagram', 'google_ads', 'tiktok']:
                # Mock actual values
                roi_actual = np.random.uniform(1.5, 4.0)
                conversion_actual = np.random.uniform(0.02, 0.15)
                
                # Mock predictions (slightly different)
                roi_pred = roi_actual * np.random.uniform(0.95, 1.05)
                conversion_pred = conversion_actual * np.random.uniform(0.95, 1.05)
                
                ts = MLROITimeSeries(
                    date=date,
                    channel=channel,
                    roi_actual=round(roi_actual, 2),
                    conversion_actual=round(conversion_actual, 4),
                    roi_pred=round(roi_pred, 2),
                    conversion_pred=round(conversion_pred, 4)
                )
                timeseries.append(ts)
        
        self.db.add_all(timeseries)
        self.db.commit()
        
        # Generate chart
        self._create_roi_timeseries_chart(timeseries)
    
    def _generate_reach_ctr_timeseries(self):
        """Generate reach and CTR timeseries"""
        timeseries = []
        for i in range(30):  # Last 30 days
            date = datetime.now().date() - timedelta(days=i)
            
            for channel in ['facebook', 'instagram', 'google_ads', 'tiktok']:
                # Mock actual values
                reach_actual = np.random.randint(5000, 50000)
                ctr_actual = np.random.uniform(0.01, 0.08)
                
                # Mock predictions
                reach_pred = int(reach_actual * np.random.uniform(0.95, 1.05))
                ctr_pred = ctr_actual * np.random.uniform(0.95, 1.05)
                
                ts = MLReachCTRTimeSeries(
                    date=date,
                    channel=channel,
                    reach_actual=reach_actual,
                    ctr_actual=round(ctr_actual, 4),
                    reach_pred=reach_pred,
                    ctr_pred=round(ctr_pred, 4)
                )
                timeseries.append(ts)
        
        self.db.add_all(timeseries)
        self.db.commit()
        
        # Generate chart
        self._create_reach_ctr_chart(timeseries)
    
    def _generate_budget_recommendations(self):
        """Generate budget recommendations"""
        campaigns = self.db.query(Campaign).all()
        df = pd.DataFrame([{
            'channel': c.channel,
            'roi': c.roi,
            'conversion_rate': c.conversion_rate,
            'cost': c.cost
        } for c in campaigns])
        
        recommendations = []
        for channel in df['channel'].unique():
            channel_data = df[df['channel'] == channel]
            
            # Calculate recommendations
            avg_roi = channel_data['roi'].mean()
            avg_conversion = channel_data['conversion_rate'].mean()
            avg_cost = channel_data['cost'].mean()
            
            # Recommend budget based on performance
            if avg_roi > 3.0:
                budget_change = np.random.uniform(0.15, 0.30)  # Increase 15-30%
            elif avg_roi > 2.0:
                budget_change = np.random.uniform(0.05, 0.15)  # Increase 5-15%
            else:
                budget_change = np.random.uniform(-0.20, 0.05)  # Decrease or small increase
            
            recommended_budget = avg_cost * (1 + budget_change)
            
            rec = MLBudgetRec(
                channel=channel,
                roi_pred=round(avg_roi * 1.1, 2),  # Predicted improvement
                conversion_pred=round(avg_conversion * 1.05, 4),
                acquisition_cost=round(avg_cost, 2),
                recommended_budget=round(recommended_budget, 2),
                budget_change_pct=round(budget_change * 100, 1)
            )
            recommendations.append(rec)
        
        self.db.add_all(recommendations)
        self.db.commit()
        
        # Generate chart
        self._create_budget_rec_chart(recommendations)
    
    def _create_roi_forecast_chart(self, forecasts: List[MLROIForecast]):
        """Create ROI forecast chart"""
        plt.figure(figsize=(10, 6))
        
        channels = [f.channel for f in forecasts]
        roi_values = [f.roi_forecast for f in forecasts]
        confidence = [f.confidence_score for f in forecasts]
        
        bars = plt.bar(channels, roi_values, alpha=0.8)
        
        # Add confidence as text on bars
        for bar, conf in zip(bars, confidence):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{conf:.0%}', ha='center', va='bottom', fontsize=9)
        
        plt.title('ROI Forecast by Channel', fontsize=14, fontweight='bold')
        plt.xlabel('Channel')
        plt.ylabel('Predicted ROI')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save chart
        chart_path = os.path.join(self.output_dir, 'roi_forecast.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Save to database
        self._save_chart_to_db('roi_forecast', chart_path)
    
    def _create_roi_timeseries_chart(self, timeseries: List[MLROITimeSeries]):
        """Create ROI timeseries chart"""
        df = pd.DataFrame([{
            'date': ts.date,
            'channel': ts.channel,
            'roi_actual': ts.roi_actual,
            'roi_pred': ts.roi_pred
        } for ts in timeseries])
        
        plt.figure(figsize=(12, 8))
        
        for i, channel in enumerate(df['channel'].unique()):
            channel_data = df[df['channel'] == channel].sort_values('date')
            
            plt.subplot(2, 2, i+1)
            plt.plot(channel_data['date'], channel_data['roi_actual'], 
                    label='Actual', marker='o', markersize=3)
            plt.plot(channel_data['date'], channel_data['roi_pred'], 
                    label='Predicted', marker='s', markersize=3, alpha=0.7)
            
            plt.title(f'{channel.title()} ROI Trend')
            plt.xlabel('Date')
            plt.ylabel('ROI')
            plt.legend()
            plt.xticks(rotation=45)
        
        plt.suptitle('ROI Trends: Actual vs Predicted', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        chart_path = os.path.join(self.output_dir, 'roi_timeseries.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self._save_chart_to_db('roi_timeseries', chart_path)
    
    def _create_reach_ctr_chart(self, timeseries: List[MLReachCTRTimeSeries]):
        """Create reach and CTR chart"""
        df = pd.DataFrame([{
            'date': ts.date,
            'channel': ts.channel,
            'reach_actual': ts.reach_actual,
            'ctr_actual': ts.ctr_actual
        } for ts in timeseries])
        
        plt.figure(figsize=(12, 6))
        
        # Reach chart
        plt.subplot(1, 2, 1)
        for channel in df['channel'].unique():
            channel_data = df[df['channel'] == channel].sort_values('date')
            plt.plot(channel_data['date'], channel_data['reach_actual'], 
                    label=channel, marker='o', markersize=2)
        
        plt.title('Reach Over Time')
        plt.xlabel('Date')
        plt.ylabel('Reach')
        plt.legend()
        plt.xticks(rotation=45)
        
        # CTR chart
        plt.subplot(1, 2, 2)
        for channel in df['channel'].unique():
            channel_data = df[df['channel'] == channel].sort_values('date')
            plt.plot(channel_data['date'], channel_data['ctr_actual'], 
                    label=channel, marker='s', markersize=2)
        
        plt.title('CTR Over Time')
        plt.xlabel('Date')
        plt.ylabel('CTR')
        plt.legend()
        plt.xticks(rotation=45)
        
        plt.suptitle('Reach & CTR Trends by Channel', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        chart_path = os.path.join(self.output_dir, 'reach_ctr_timeseries.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self._save_chart_to_db('reach_ctr_timeseries', chart_path)
    
    def _create_budget_rec_chart(self, recommendations: List[MLBudgetRec]):
        """Create budget recommendations chart"""
        plt.figure(figsize=(10, 6))
        
        channels = [r.channel for r in recommendations]
        budget_changes = [r.budget_change_pct for r in recommendations]
        
        colors = ['green' if x > 0 else 'red' for x in budget_changes]
        bars = plt.bar(channels, budget_changes, color=colors, alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, budget_changes):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., 
                    height + (1 if height > 0 else -3),
                    f'{value:+.1f}%', ha='center', va='bottom' if height > 0 else 'top')
        
        plt.title('Budget Change Recommendations by Channel', fontsize=14, fontweight='bold')
        plt.xlabel('Channel')
        plt.ylabel('Budget Change (%)')
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        chart_path = os.path.join(self.output_dir, 'budget_recommendations.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self._save_chart_to_db('budget_recommendations', chart_path)
    
    def _save_chart_to_db(self, dashboard_type: str, chart_path: str):
        """Save chart to database as binary data"""
        with open(chart_path, 'rb') as f:
            image_data = f.read()
        
        # Remove old chart of same type
        self.db.query(MLDashboard).filter(
            MLDashboard.dashboard_type == dashboard_type
        ).delete()
        
        # Save new chart
        dashboard = MLDashboard(
            dashboard_type=dashboard_type,
            image_data=image_data
        )
        self.db.add(dashboard)
        self.db.commit()
