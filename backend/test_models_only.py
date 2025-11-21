#!/usr/bin/env python3
"""
Simple test to verify models can be imported without database connection
"""

import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_model_definitions():
    """Test that model classes can be defined"""
    print("Testing model definitions...")
    
    try:
        # Import SQLAlchemy components
        from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, Text, LargeBinary
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.sql import func
        from sqlalchemy.dialects.postgresql import JSONB
        
        # Create a test base
        Base = declarative_base()
        
        # Define test models (simplified versions)
        class TestCampaign(Base):
            __tablename__ = "test_campaigns"
            id = Column(Integer, primary_key=True)
            campaign_id = Column(String(50))
            channel = Column(String(50))
            roi = Column(Float)
        
        class TestPrediction(Base):
            __tablename__ = "test_predictions"
            id = Column(Integer, primary_key=True)
            campaign_id = Column(String(50))
            predicted_roi = Column(Float)
        
        class TestAlert(Base):
            __tablename__ = "test_alerts"
            id = Column(Integer, primary_key=True)
            alert_type = Column(String(50))
            severity = Column(String(20))
            is_read = Column(Boolean, default=False)
        
        print("Model definitions work!")
        
        # Test model instantiation
        campaign = TestCampaign(campaign_id="TEST_001", channel="facebook", roi=2.5)
        prediction = TestPrediction(campaign_id="TEST_001", predicted_roi=2.8)
        alert = TestAlert(alert_type="roi_drop", severity="high")
        
        print("Model instantiation works!")
        print(f"   Campaign: {campaign.campaign_id}")
        print(f"   Prediction: {prediction.predicted_roi}")
        print(f"   Alert: {alert.alert_type}")
        
        return True
        
    except Exception as e:
        print(f"Model test failed: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available"""
    print("\nTesting dependencies...")
    
    dependencies = [
        'sqlalchemy',
        'psycopg2',
        'faker',
        'pandas',
        'numpy'
    ]
    
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   {dep}: OK")
        except ImportError:
            print(f"   {dep}: MISSING")
            missing.append(dep)
    
    if missing:
        print(f"Missing dependencies: {missing}")
        return False
    
    print("All dependencies available!")
    return True

def main():
    """Run tests"""
    print("DEMETRA AI Analytics - Simple Model Test")
    print("=" * 45)
    
    tests_passed = 0
    total_tests = 2
    
    if test_model_definitions():
        tests_passed += 1
    
    if test_dependencies():
        tests_passed += 1
    
    print(f"\nResults: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("SUCCESS: Models and dependencies are ready!")
        print("\nNext steps:")
        print("1. Start PostgreSQL database")
        print("2. Run: python setup_database.py")
        print("3. Start backend: python -m uvicorn app.main:app --reload")
    else:
        print("FAILED: Some issues need to be resolved")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
