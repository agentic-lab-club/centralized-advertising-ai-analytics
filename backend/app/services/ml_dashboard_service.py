import os
import io
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import MLROIForecast, MLROITimeSeries, MLReachCTRTimeSeries, MLBudgetRec
from app.configs.database import get_db, engine

class MLDashboardService:
    def __init__(self):
        self.static_dir = "/mnt/d/Hackathons/MEITU-university-advertisement_compaign_centralized_ai_system/centralized-advertising-ai-analytics/backend/static"
        os.makedirs(self.static_dir, exist_ok=True)
    
    def ensure_tables_exist(self, db: Session):
        """Create ML tables if they don't exist"""
        try:
            # Try to create tables
            from app.configs.database import Base
            Base.metadata.create_all(bind=engine)
            return True
        except Exception as e:
            print(f"Warning: Could not create tables: {e}")
            return False
    
    def table_exists(self, db: Session, table_name: str) -> bool:
        """Check if a table exists"""
        try:
            result = db.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
            return True
        except Exception:
            return False
        
    def generate_sample_data(self):
        """Generate sample ML data for dashboards"""
        channels = ["Facebook", "Instagram", "Twitter", "Pinterest"]
        dates = pd.date_range(start="2024-01-01", end="2024-11-22", freq="D")
        
        # Sample ROI forecast data
        roi_data = []
        for channel in channels:
            roi_forecast = np.random.uniform(0.5, 3.5, 1)[0]
            roi_data.append({
                "channel": channel,
                "roi_forecast": round(roi_forecast, 3),
                "confidence_score": np.random.uniform(0.7, 0.95)
            })
        
        # Sample time series data
        timeseries_data = []
        reach_ctr_data = []
        
        for date in dates[-30:]:  # Last 30 days
            for channel in channels:
                # ROI timeseries
                timeseries_data.append({
                    "date": date.date(),
                    "channel": channel,
                    "roi_actual": np.random.uniform(1.0, 4.0),
                    "conversion_actual": np.random.uniform(0.05, 0.15),
                    "roi_pred": np.random.uniform(1.0, 4.0),
                    "conversion_pred": np.random.uniform(0.05, 0.15)
                })
                
                # Reach/CTR timeseries
                reach_ctr_data.append({
                    "date": date.date(),
                    "channel": channel,
                    "reach_actual": np.random.randint(1000, 10000),
                    "ctr_actual": np.random.uniform(0.01, 0.08),
                    "reach_pred": np.random.randint(1000, 10000),
                    "ctr_pred": np.random.uniform(0.01, 0.08)
                })
        
        # Budget recommendations
        budget_data = []
        total_budget = 100000
        weights = np.random.dirichlet(np.ones(len(channels)))
        
        for i, channel in enumerate(channels):
            budget_data.append({
                "channel": channel,
                "roi_pred": np.random.uniform(2.0, 4.0),
                "conversion_pred": np.random.uniform(0.06, 0.12),
                "acquisition_cost": np.random.uniform(5000, 8000),
                "recommended_budget": round(total_budget * weights[i], 2),
                "total_budget": total_budget
            })
        
        return roi_data, timeseries_data, reach_ctr_data, budget_data
    
    def save_to_database(self, db: Session):
        """Save generated data to database tables"""
        # Ensure tables exist first
        if not self.ensure_tables_exist(db):
            raise Exception("Could not create ML tables")
        
        roi_data, timeseries_data, reach_ctr_data, budget_data = self.generate_sample_data()
        
        try:
            # Clear existing data only if tables exist
            if self.table_exists(db, "ml_roi_forecast"):
                db.query(MLROIForecast).delete()
            if self.table_exists(db, "ml_roi_timeseries"):
                db.query(MLROITimeSeries).delete()
            if self.table_exists(db, "ml_reach_ctr_timeseries"):
                db.query(MLReachCTRTimeSeries).delete()
            if self.table_exists(db, "ml_budget_rec"):
                db.query(MLBudgetRec).delete()
            
            # Insert new data
            for item in roi_data:
                db.add(MLROIForecast(**item))
            
            for item in timeseries_data:
                db.add(MLROITimeSeries(**item))
            
            for item in reach_ctr_data:
                db.add(MLReachCTRTimeSeries(**item))
            
            for item in budget_data:
                db.add(MLBudgetRec(**item))
            
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Database error: {e}")
    
    def generate_roi_forecast_chart(self, db: Session) -> str:
        """Generate ROI forecast by channel chart"""
        try:
            forecasts = db.query(MLROIForecast).all()
            if not forecasts:
                # Generate sample data if no data exists
                self.save_to_database(db)
                forecasts = db.query(MLROIForecast).all()
            
            df = pd.DataFrame([{
                "Channel": f.channel,
                "ROI_Forecast": f.roi_forecast
            } for f in forecasts])
            
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x="Channel", y="ROI_Forecast", hue="Channel", palette="viridis", legend=False)
            plt.title("Прогнозируемый ROI по каналам", fontsize=16)
            plt.xlabel("Канал")
            plt.ylabel("Прогнозный ROI")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            chart_path = os.path.join(self.static_dir, "roi_forecast_by_channel.png")
            plt.savefig(chart_path, dpi=300, bbox_inches="tight")
            plt.close()
            return chart_path
        except Exception as e:
            # Generate dummy chart if database fails
            return self.generate_dummy_chart("ROI Forecast", "roi_forecast_by_channel.png")
    
    def generate_dummy_chart(self, title: str, filename: str) -> str:
        """Generate a dummy chart when database is not available"""
        plt.figure(figsize=(10, 6))
        channels = ["Facebook", "Instagram", "Twitter", "Pinterest"]
        values = [3.2, 2.8, 2.5, 1.8]
        
        plt.bar(channels, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        plt.title(f"{title} (Sample Data)", fontsize=16)
        plt.xlabel("Channel")
        plt.ylabel("Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        chart_path = os.path.join(self.static_dir, filename)
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_roi_timeseries_chart(self, db: Session) -> str:
        """Generate ROI and conversion over time chart"""
        try:
            timeseries = db.query(MLROITimeSeries).all()
            if not timeseries:
                self.save_to_database(db)
                timeseries = db.query(MLROITimeSeries).all()
            
            df = pd.DataFrame([{
                "Date": t.date,
                "Channel": t.channel,
                "ROI_Actual": t.roi_actual,
                "Conversion_Actual": t.conversion_actual
            } for t in timeseries])
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # ROI over time
            for channel in df["Channel"].unique():
                channel_data = df[df["Channel"] == channel]
                ax1.plot(channel_data["Date"], channel_data["ROI_Actual"], label=channel, marker='o')
            ax1.set_title("ROI по времени")
            ax1.set_ylabel("ROI")
            ax1.legend()
            ax1.grid(True)
            
            # Conversion over time
            for channel in df["Channel"].unique():
                channel_data = df[df["Channel"] == channel]
                ax2.plot(channel_data["Date"], channel_data["Conversion_Actual"], label=channel, marker='s')
            ax2.set_title("Конверсия по времени")
            ax2.set_ylabel("Конверсия")
            ax2.set_xlabel("Дата")
            ax2.legend()
            ax2.grid(True)
            
            plt.tight_layout()
            chart_path = os.path.join(self.static_dir, "roi_conversion_timeseries.png")
            plt.savefig(chart_path, dpi=300, bbox_inches="tight")
            plt.close()
            return chart_path
        except Exception as e:
            return self.generate_dummy_chart("ROI Timeseries", "roi_conversion_timeseries.png")
    
    def generate_reach_ctr_chart(self, db: Session) -> str:
        """Generate reach and CTR over time chart"""
        try:
            reach_ctr = db.query(MLReachCTRTimeSeries).all()
            if not reach_ctr:
                self.save_to_database(db)
                reach_ctr = db.query(MLReachCTRTimeSeries).all()
            
            df = pd.DataFrame([{
                "Date": r.date,
                "Channel": r.channel,
                "Reach": r.reach_actual,
                "CTR": r.ctr_actual
            } for r in reach_ctr])
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Reach over time
            for channel in df["Channel"].unique():
                channel_data = df[df["Channel"] == channel]
                ax1.plot(channel_data["Date"], channel_data["Reach"], label=channel, marker='o')
            ax1.set_title("Охват по времени")
            ax1.set_ylabel("Охват")
            ax1.legend()
            ax1.grid(True)
            
            # CTR over time
            for channel in df["Channel"].unique():
                channel_data = df[df["Channel"] == channel]
                ax2.plot(channel_data["Date"], channel_data["CTR"], label=channel, marker='s')
            ax2.set_title("CTR по времени")
            ax2.set_ylabel("CTR")
            ax2.set_xlabel("Дата")
            ax2.legend()
            ax2.grid(True)
            
            plt.tight_layout()
            chart_path = os.path.join(self.static_dir, "reach_ctr_timeseries.png")
            plt.savefig(chart_path, dpi=300, bbox_inches="tight")
            plt.close()
            return chart_path
        except Exception as e:
            return self.generate_dummy_chart("Reach CTR", "reach_ctr_timeseries.png")
    
    def generate_budget_recommendation_chart(self, db: Session) -> str:
        """Generate budget recommendation chart"""
        try:
            budget_recs = db.query(MLBudgetRec).all()
            if not budget_recs:
                self.save_to_database(db)
                budget_recs = db.query(MLBudgetRec).all()
            
            df = pd.DataFrame([{
                "Channel": b.channel,
                "Recommended_Budget": b.recommended_budget,
                "ROI_Pred": b.roi_pred
            } for b in budget_recs])
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Budget allocation
            sns.barplot(data=df, x="Channel", y="Recommended_Budget", hue="Channel", ax=ax1, palette="Set2", legend=False)
            ax1.set_title("Рекомендуемое распределение бюджета")
            ax1.set_ylabel("Бюджет")
            ax1.tick_params(axis='x', rotation=45)
            
            # ROI prediction
            sns.barplot(data=df, x="Channel", y="ROI_Pred", hue="Channel", ax=ax2, palette="Set1", legend=False)
            ax2.set_title("Прогнозируемый ROI")
            ax2.set_ylabel("ROI")
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            chart_path = os.path.join(self.static_dir, "budget_recommendation.png")
            plt.savefig(chart_path, dpi=300, bbox_inches="tight")
            plt.close()
            return chart_path
        except Exception as e:
            return self.generate_dummy_chart("Budget Recommendation", "budget_recommendation.png")
    
    def generate_all_dashboards(self, db: Session):
        """Generate all ML dashboards and save to database"""
        try:
            # Ensure tables exist and save data
            self.save_to_database(db)
            
            # Generate all charts
            charts = {
                "roi_forecast": self.generate_roi_forecast_chart(db),
                "roi_timeseries": self.generate_roi_timeseries_chart(db),
                "reach_ctr": self.generate_reach_ctr_chart(db),
                "budget_recommendation": self.generate_budget_recommendation_chart(db)
            }
            
            return charts
        except Exception as e:
            # Generate dummy charts if database fails
            return {
                "roi_forecast": self.generate_dummy_chart("ROI Forecast", "roi_forecast_by_channel.png"),
                "roi_timeseries": self.generate_dummy_chart("ROI Timeseries", "roi_conversion_timeseries.png"),
                "reach_ctr": self.generate_dummy_chart("Reach CTR", "reach_ctr_timeseries.png"),
                "budget_recommendation": self.generate_dummy_chart("Budget Rec", "budget_recommendation.png")
            }

class MLDashboardService:
    def __init__(self):
        self.static_dir = "/mnt/d/Hackathons/MEITU-university-advertisement_compaign_centralized_ai_system/centralized-advertising-ai-analytics/backend/static"
        os.makedirs(self.static_dir, exist_ok=True)
        
    def generate_sample_data(self):
        """Generate sample ML data for dashboards"""
        channels = ["Facebook", "Instagram", "Twitter", "Pinterest"]
        dates = pd.date_range(start="2024-01-01", end="2024-11-22", freq="D")
        
        # Sample ROI forecast data
        roi_data = []
        for channel in channels:
            roi_forecast = np.random.uniform(0.5, 3.5, 1)[0]
            roi_data.append({
                "channel": channel,
                "roi_forecast": round(roi_forecast, 3),
                "confidence_score": np.random.uniform(0.7, 0.95)
            })
        
        # Sample time series data
        timeseries_data = []
        reach_ctr_data = []
        
        for date in dates[-30:]:  # Last 30 days
            for channel in channels:
                # ROI timeseries
                timeseries_data.append({
                    "date": date.date(),
                    "channel": channel,
                    "roi_actual": np.random.uniform(1.0, 4.0),
                    "conversion_actual": np.random.uniform(0.05, 0.15),
                    "roi_pred": np.random.uniform(1.0, 4.0),
                    "conversion_pred": np.random.uniform(0.05, 0.15)
                })
                
                # Reach/CTR timeseries
                reach_ctr_data.append({
                    "date": date.date(),
                    "channel": channel,
                    "reach_actual": np.random.randint(1000, 10000),
                    "ctr_actual": np.random.uniform(0.01, 0.08),
                    "reach_pred": np.random.randint(1000, 10000),
                    "ctr_pred": np.random.uniform(0.01, 0.08)
                })
        
        # Budget recommendations
        budget_data = []
        total_budget = 100000
        weights = np.random.dirichlet(np.ones(len(channels)))
        
        for i, channel in enumerate(channels):
            budget_data.append({
                "channel": channel,
                "roi_pred": np.random.uniform(2.0, 4.0),
                "conversion_pred": np.random.uniform(0.06, 0.12),
                "acquisition_cost": np.random.uniform(5000, 8000),
                "recommended_budget": round(total_budget * weights[i], 2),
                "total_budget": total_budget
            })
        
        return roi_data, timeseries_data, reach_ctr_data, budget_data
    
    def save_to_database(self, db: Session):
        """Save generated data to database tables"""
        roi_data, timeseries_data, reach_ctr_data, budget_data = self.generate_sample_data()
        
        # Clear existing data
        db.query(MLROIForecast).delete()
        db.query(MLROITimeSeries).delete()
        db.query(MLReachCTRTimeSeries).delete()
        db.query(MLBudgetRec).delete()
        
        # Insert ROI forecasts
        for item in roi_data:
            db.add(MLROIForecast(**item))
        
        # Insert timeseries data
        for item in timeseries_data:
            db.add(MLROITimeSeries(**item))
        
        for item in reach_ctr_data:
            db.add(MLReachCTRTimeSeries(**item))
        
        # Insert budget recommendations
        for item in budget_data:
            db.add(MLBudgetRec(**item))
        
        db.commit()
    
    def generate_roi_forecast_chart(self, db: Session) -> str:
        """Generate ROI forecast by channel chart"""
        forecasts = db.query(MLROIForecast).all()
        df = pd.DataFrame([{
            "Channel": f.channel,
            "ROI_Forecast": f.roi_forecast
        } for f in forecasts])
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x="Channel", y="ROI_Forecast", hue="Channel", palette="viridis", legend=False)
        plt.title("Прогнозируемый ROI по каналам", fontsize=16)
        plt.xlabel("Канал")
        plt.ylabel("Прогнозный ROI")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        chart_path = os.path.join(self.static_dir, "roi_forecast_by_channel.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_roi_timeseries_chart(self, db: Session) -> str:
        """Generate ROI and conversion over time chart"""
        timeseries = db.query(MLROITimeSeries).all()
        df = pd.DataFrame([{
            "Date": t.date,
            "Channel": t.channel,
            "ROI_Actual": t.roi_actual,
            "Conversion_Actual": t.conversion_actual
        } for t in timeseries])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # ROI over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax1.plot(channel_data["Date"], channel_data["ROI_Actual"], label=channel, marker='o')
        ax1.set_title("ROI по времени")
        ax1.set_ylabel("ROI")
        ax1.legend()
        ax1.grid(True)
        
        # Conversion over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax2.plot(channel_data["Date"], channel_data["Conversion_Actual"], label=channel, marker='s')
        ax2.set_title("Конверсия по времени")
        ax2.set_ylabel("Конверсия")
        ax2.set_xlabel("Дата")
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        chart_path = os.path.join(self.static_dir, "roi_conversion_timeseries.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_reach_ctr_chart(self, db: Session) -> str:
        """Generate reach and CTR over time chart"""
        reach_ctr = db.query(MLReachCTRTimeSeries).all()
        df = pd.DataFrame([{
            "Date": r.date,
            "Channel": r.channel,
            "Reach": r.reach_actual,
            "CTR": r.ctr_actual
        } for r in reach_ctr])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Reach over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax1.plot(channel_data["Date"], channel_data["Reach"], label=channel, marker='o')
        ax1.set_title("Охват по времени")
        ax1.set_ylabel("Охват")
        ax1.legend()
        ax1.grid(True)
        
        # CTR over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax2.plot(channel_data["Date"], channel_data["CTR"], label=channel, marker='s')
        ax2.set_title("CTR по времени")
        ax2.set_ylabel("CTR")
        ax2.set_xlabel("Дата")
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        chart_path = os.path.join(self.static_dir, "reach_ctr_timeseries.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_budget_recommendation_chart(self, db: Session) -> str:
        """Generate budget recommendation chart"""
        budget_recs = db.query(MLBudgetRec).all()
        df = pd.DataFrame([{
            "Channel": b.channel,
            "Recommended_Budget": b.recommended_budget,
            "ROI_Pred": b.roi_pred
        } for b in budget_recs])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Budget allocation
        sns.barplot(data=df, x="Channel", y="Recommended_Budget", hue="Channel", ax=ax1, palette="Set2", legend=False)
        ax1.set_title("Рекомендуемое распределение бюджета")
        ax1.set_ylabel("Бюджет")
        ax1.tick_params(axis='x', rotation=45)
        
        # ROI prediction
        sns.barplot(data=df, x="Channel", y="ROI_Pred", hue="Channel", ax=ax2, palette="Set1", legend=False)
        ax2.set_title("Прогнозируемый ROI")
        ax2.set_ylabel("ROI")
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        chart_path = os.path.join(self.static_dir, "budget_recommendation.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_all_dashboards(self, db: Session):
        """Generate all ML dashboards and save to database"""
        # Save data to database
        self.save_to_database(db)
        
        # Generate all charts
        charts = {
            "roi_forecast": self.generate_roi_forecast_chart(db),
            "roi_timeseries": self.generate_roi_timeseries_chart(db),
            "reach_ctr": self.generate_reach_ctr_chart(db),
            "budget_recommendation": self.generate_budget_recommendation_chart(db)
        }
        
        return charts

class MLDashboardService:
    def __init__(self):
        self.static_dir = "/mnt/d/Hackathons/MEITU-university-advertisement_compaign_centralized_ai_system/centralized-advertising-ai-analytics/backend/static"
        os.makedirs(self.static_dir, exist_ok=True)
        
    def generate_sample_data(self):
        """Generate sample ML data for dashboards"""
        channels = ["Facebook", "Instagram", "Twitter", "Pinterest"]
        dates = pd.date_range(start="2024-01-01", end="2024-11-22", freq="D")
        
        # Sample ROI forecast data
        roi_data = []
        for channel in channels:
            roi_forecast = np.random.uniform(0.5, 3.5, 1)[0]
            roi_data.append({
                "channel": channel,
                "roi_forecast": round(roi_forecast, 3),
                "confidence_score": np.random.uniform(0.7, 0.95)
            })
        
        # Sample time series data
        timeseries_data = []
        reach_ctr_data = []
        
        for date in dates[-30:]:  # Last 30 days
            for channel in channels:
                # ROI timeseries
                timeseries_data.append({
                    "date": date.date(),
                    "channel": channel,
                    "roi_actual": np.random.uniform(1.0, 4.0),
                    "conversion_actual": np.random.uniform(0.05, 0.15),
                    "roi_pred": np.random.uniform(1.0, 4.0),
                    "conversion_pred": np.random.uniform(0.05, 0.15)
                })
                
                # Reach/CTR timeseries
                reach_ctr_data.append({
                    "date": date.date(),
                    "channel": channel,
                    "reach_actual": np.random.randint(1000, 10000),
                    "ctr_actual": np.random.uniform(0.01, 0.08),
                    "reach_pred": np.random.randint(1000, 10000),
                    "ctr_pred": np.random.uniform(0.01, 0.08)
                })
        
        # Budget recommendations
        budget_data = []
        total_budget = 100000
        weights = np.random.dirichlet(np.ones(len(channels)))
        
        for i, channel in enumerate(channels):
            budget_data.append({
                "channel": channel,
                "roi_pred": np.random.uniform(2.0, 4.0),
                "conversion_pred": np.random.uniform(0.06, 0.12),
                "acquisition_cost": np.random.uniform(5000, 8000),
                "recommended_budget": round(total_budget * weights[i], 2)
            })
        
        return roi_data, timeseries_data, reach_ctr_data, budget_data
    
    def save_to_database(self, db: Session):
        """Save generated data to database tables"""
        roi_data, timeseries_data, reach_ctr_data, budget_data = self.generate_sample_data()
        
        # Clear existing data
        db.query(MLROIForecast).delete()
        db.query(MLROITimeSeries).delete()
        db.query(MLReachCTRTimeSeries).delete()
        db.query(MLBudgetRec).delete()
        
        # Insert ROI forecasts
        for item in roi_data:
            db.add(MLROIForecast(**item))
        
        # Insert timeseries data
        for item in timeseries_data:
            db.add(MLROITimeSeries(**item))
        
        for item in reach_ctr_data:
            db.add(MLReachCTRTimeSeries(**item))
        
        # Insert budget recommendations
        for item in budget_data:
            db.add(MLBudgetRec(**item))
        
        db.commit()
    
    def generate_roi_forecast_chart(self, db: Session) -> str:
        """Generate ROI forecast by channel chart"""
        forecasts = db.query(MLROIForecast).all()
        df = pd.DataFrame([{
            "Channel": f.channel,
            "ROI_Forecast": f.roi_forecast
        } for f in forecasts])
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x="Channel", y="ROI_Forecast", hue="Channel", palette="viridis", legend=False)
        plt.title("Прогнозируемый ROI по каналам", fontsize=16)
        plt.xlabel("Канал")
        plt.ylabel("Прогнозный ROI")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        chart_path = os.path.join(self.static_dir, "roi_forecast_by_channel.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_roi_timeseries_chart(self, db: Session) -> str:
        """Generate ROI and conversion over time chart"""
        timeseries = db.query(MLROITimeSeries).all()
        df = pd.DataFrame([{
            "Date": t.date,
            "Channel": t.channel,
            "ROI_Actual": t.roi_actual,
            "Conversion_Actual": t.conversion_actual
        } for t in timeseries])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # ROI over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax1.plot(channel_data["Date"], channel_data["ROI_Actual"], label=channel, marker='o')
        ax1.set_title("ROI по времени")
        ax1.set_ylabel("ROI")
        ax1.legend()
        ax1.grid(True)
        
        # Conversion over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax2.plot(channel_data["Date"], channel_data["Conversion_Actual"], label=channel, marker='s')
        ax2.set_title("Конверсия по времени")
        ax2.set_ylabel("Конверсия")
        ax2.set_xlabel("Дата")
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        chart_path = os.path.join(self.static_dir, "roi_conversion_timeseries.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_reach_ctr_chart(self, db: Session) -> str:
        """Generate reach and CTR over time chart"""
        reach_ctr = db.query(MLReachCTRTimeSeries).all()
        df = pd.DataFrame([{
            "Date": r.date,
            "Channel": r.channel,
            "Reach": r.reach_actual,
            "CTR": r.ctr_actual
        } for r in reach_ctr])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Reach over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax1.plot(channel_data["Date"], channel_data["Reach"], label=channel, marker='o')
        ax1.set_title("Охват по времени")
        ax1.set_ylabel("Охват")
        ax1.legend()
        ax1.grid(True)
        
        # CTR over time
        for channel in df["Channel"].unique():
            channel_data = df[df["Channel"] == channel]
            ax2.plot(channel_data["Date"], channel_data["CTR"], label=channel, marker='s')
        ax2.set_title("CTR по времени")
        ax2.set_ylabel("CTR")
        ax2.set_xlabel("Дата")
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        chart_path = os.path.join(self.static_dir, "reach_ctr_timeseries.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_budget_recommendation_chart(self, db: Session) -> str:
        """Generate budget recommendation chart"""
        budget_recs = db.query(MLBudgetRec).all()
        df = pd.DataFrame([{
            "Channel": b.channel,
            "Recommended_Budget": b.recommended_budget,
            "ROI_Pred": b.roi_pred
        } for b in budget_recs])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Budget allocation
        sns.barplot(data=df, x="Channel", y="Recommended_Budget", hue="Channel", ax=ax1, palette="Set2", legend=False)
        ax1.set_title("Рекомендуемое распределение бюджета")
        ax1.set_ylabel("Бюджет")
        ax1.tick_params(axis='x', rotation=45)
        
        # ROI prediction
        sns.barplot(data=df, x="Channel", y="ROI_Pred", hue="Channel", ax=ax2, palette="Set1", legend=False)
        ax2.set_title("Прогнозируемый ROI")
        ax2.set_ylabel("ROI")
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        chart_path = os.path.join(self.static_dir, "budget_recommendation.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        return chart_path
    
    def generate_all_dashboards(self, db: Session):
        """Generate all ML dashboards and save to database"""
        # Save data to database
        self.save_to_database(db)
        
        # Generate all charts
        charts = {
            "roi_forecast": self.generate_roi_forecast_chart(db),
            "roi_timeseries": self.generate_roi_timeseries_chart(db),
            "reach_ctr": self.generate_reach_ctr_chart(db),
            "budget_recommendation": self.generate_budget_recommendation_chart(db)
        }
        
        return charts
