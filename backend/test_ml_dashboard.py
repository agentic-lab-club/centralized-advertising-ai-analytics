#!/usr/bin/env python3
"""Test script for ML Dashboard functionality"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_ml_dashboard():
    """Test ML dashboard endpoints"""
    print("🧪 Testing ML Dashboard System")
    print("=" * 50)
    
    # Test 1: Check ML dashboard status
    print("1. Checking ML dashboard status...")
    response = requests.get(f"{BASE_URL}/api/ml-dashboard/status")
    if response.status_code == 200:
        status = response.json()
        print(f"   ✅ Status: {status['status']}")
        print(f"   📊 Predictions: {status['predictions']}")
        print(f"   📈 Charts available: {status['charts_available']}")
    else:
        print(f"   ❌ Status check failed: {response.status_code}")
        return
    
    # Test 2: Trigger ML sync
    print("2. Triggering ML predictions sync...")
    response = requests.post(f"{BASE_URL}/api/ml-dashboard/sync-now")
    if response.status_code == 200:
        print(f"   ✅ Sync completed: {response.json()['message']}")
    else:
        print(f"   ❌ Sync failed: {response.status_code}")
        return
    
    # Wait a moment for processing
    print("3. Waiting for processing...")
    time.sleep(3)
    
    # Test 3: Check ROI forecast data
    print("4. Testing ROI forecast data...")
    response = requests.get(f"{BASE_URL}/api/ml-dashboard/roi-forecast/data")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ ROI forecasts: {len(data)} channels")
        for item in data[:3]:  # Show first 3
            print(f"      {item['channel']}: {item['roi_forecast']:.2f}")
    else:
        print(f"   ❌ ROI data failed: {response.status_code}")
    
    # Test 4: Check chart availability
    print("5. Testing chart endpoints...")
    charts = [
        ("ROI Forecast", "/api/ml-dashboard/roi-forecast/chart"),
        ("ROI Timeseries", "/api/ml-dashboard/roi-timeseries/chart"),
        ("Reach CTR", "/api/ml-dashboard/reach-ctr/chart"),
        ("Budget Rec", "/api/ml-dashboard/budget-recommendation/chart")
    ]
    
    for name, endpoint in charts:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            print(f"   ✅ {name} chart available ({len(response.content)} bytes)")
        else:
            print(f"   ❌ {name} chart failed: {response.status_code}")
    
    print("\n🎉 ML Dashboard test completed!")

if __name__ == "__main__":
    test_ml_dashboard()
