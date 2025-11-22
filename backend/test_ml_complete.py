#!/usr/bin/env python3
"""
Complete ML Dashboard System Test
Tests all ML dashboard endpoints, scheduler, and data generation
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"{method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            if 'image/png' in response.headers.get('content-type', ''):
                print(f"  ✅ PNG chart received ({len(response.content)} bytes)")
            else:
                result = response.json()
                print(f"  ✅ {json.dumps(result, indent=2)[:200]}...")
        else:
            print(f"  ❌ Error: {response.text}")
        return response
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return None

def main():
    print("🚀 TESTING COMPLETE ML DASHBOARD SYSTEM")
    print("=" * 50)
    
    # 1. Test basic health
    print("\n1. Testing API Health...")
    test_endpoint("GET", "/health")
    test_endpoint("GET", "/api/test")
    
    # 2. Test scheduler status
    print("\n2. Testing Scheduler...")
    test_endpoint("GET", "/api/sync/status")
    
    # 3. Generate sample data
    print("\n3. Generating Sample ML Data...")
    test_endpoint("POST", "/api/sync/generate-sample-data")
    
    # 4. Test manual sync
    print("\n4. Testing Manual Sync...")
    test_endpoint("POST", "/api/sync/run-now")
    
    # 5. Test all ML dashboard endpoints
    print("\n5. Testing ML Dashboard Endpoints...")
    
    # ROI Forecast
    print("\n  📊 ROI Forecast Dashboard:")
    test_endpoint("GET", "/api/ml-dashboard/roi-forecast/chart")
    test_endpoint("GET", "/api/ml-dashboard/roi-forecast/data")
    
    # ROI Timeseries
    print("\n  📈 ROI Timeseries Dashboard:")
    test_endpoint("GET", "/api/ml-dashboard/roi-timeseries/chart")
    test_endpoint("GET", "/api/ml-dashboard/roi-timeseries/data")
    
    # Reach/CTR
    print("\n  📊 Reach/CTR Dashboard:")
    test_endpoint("GET", "/api/ml-dashboard/reach-ctr/chart")
    test_endpoint("GET", "/api/ml-dashboard/reach-ctr/data")
    
    # Budget Recommendations
    print("\n  💰 Budget Recommendation Dashboard:")
    test_endpoint("GET", "/api/ml-dashboard/budget-recommendation/chart")
    test_endpoint("GET", "/api/ml-dashboard/budget-recommendation/data")
    
    # 6. Test dashboard status
    print("\n6. Testing Dashboard Status...")
    test_endpoint("GET", "/api/ml-dashboard/status")
    
    # 7. Test generate all dashboards
    print("\n7. Testing Generate All Dashboards...")
    test_endpoint("POST", "/api/ml-dashboard/generate-all")
    
    print("\n" + "=" * 50)
    print("✅ ML DASHBOARD SYSTEM TEST COMPLETE!")
    print("\n📋 FRONTEND INTEGRATION ENDPOINTS:")
    print("   - ROI Forecast Chart: GET /api/ml-dashboard/roi-forecast/chart")
    print("   - ROI Timeseries Chart: GET /api/ml-dashboard/roi-timeseries/chart")
    print("   - Reach/CTR Chart: GET /api/ml-dashboard/reach-ctr/chart")
    print("   - Budget Chart: GET /api/ml-dashboard/budget-recommendation/chart")
    print("\n🔄 SCHEDULER:")
    print("   - Runs every 30 minutes automatically")
    print("   - Manual trigger: POST /api/sync/run-now")
    print("   - Status check: GET /api/sync/status")

if __name__ == "__main__":
    main()
