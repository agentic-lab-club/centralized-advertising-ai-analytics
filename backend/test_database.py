#!/usr/bin/env python3
"""
Test script to verify database setup without requiring actual database connection
"""

import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_models():
    """Test that all models can be imported"""
    print("Testing model imports...")
    
    try:
        from app.models.campaign import Campaign
        from app.models.prediction import Prediction
        from app.models.recommendation import Recommendation
        from app.models.ml_dashboard import MLDashboard
        from app.models.alert import Alert
        
        print("All models imported successfully!")
        
        # Test model creation (without database)
        campaign = Campaign(
            campaign_id="TEST_001",
            channel="facebook",
            conversion_rate=0.05,
            cost=250.0,
            roi=2.5,
            clicks=1000,
            impressions=20000,
            engagement=150
        )
        
        print("Model instantiation works!")
        print(f"   Sample campaign: {campaign.campaign_id} - {campaign.channel}")
        
        return True
        
    except Exception as e:
        print(f"Model test failed: {e}")
        return False

def test_database_config():
    """Test database configuration"""
    print("\nTesting database configuration...")
    
    try:
        from app.configs.database import Base, SQLALCHEMY_DATABASE_URL
        
        print("Database config imported successfully!")
        print(f"   Database URL configured: {SQLALCHEMY_DATABASE_URL[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"Database config test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("DEMETRA AI Analytics - Database Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    if test_models():
        tests_passed += 1
    
    if test_database_config():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("All tests passed! Database setup is ready.")
        print("\nReady for:")
        print("   • Database migration (when DB is running)")
        print("   • Data seeding")
        print("   • API development")
    else:
        print("Some tests failed. Check the errors above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
