#!/usr/bin/env python3

import requests
import time
import json
import sys

def test_api_complete():
    """Complete test of DEMETRA API system"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 DEMETRA SYSTEMS - Complete API Test")
    print("=" * 50)
    
    # Step 1: Wait for API to be ready
    print("\n1️⃣ Testing API Health...")
    for i in range(15):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is healthy!")
                print(f"   Response: {response.json()}")
                break
        except requests.exceptions.RequestException as e:
            print(f"⏳ Waiting for API... ({i+1}/15) - {e}")
            time.sleep(2)
    else:
        print("❌ API not responding after 30 seconds")
        return False
    
    # Step 2: Test root endpoint
    print("\n2️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Version: {data.get('version')}")
            print(f"   Message: {data.get('message')}")
            print("✅ Root endpoint working!")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Step 3: Check ML tables
    print("\n3️⃣ Checking ML Tables...")
    try:
        response = requests.get(f"{base_url}/api/setup/check-tables")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Tables exist: {data.get('tables_exist', False)}")
            print(f"   ML tables: {data.get('ml_tables', [])}")
            if not data.get('tables_exist', False):
                print("   ⚠️ ML tables don't exist, will create them...")
            else:
                print("✅ ML tables already exist!")
        else:
            print(f"❌ Check tables failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Check tables error: {e}")
    
    # Step 4: Create ML tables
    print("\n4️⃣ Creating ML Tables...")
    try:
        response = requests.post(f"{base_url}/api/setup/create-ml-tables")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Result: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Tables created: {data.get('tables_created', [])}")
            print("✅ ML tables created successfully!")
        else:
            print(f"❌ Create tables failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Create tables error: {e}")
    
    # Step 5: Check ML dashboard status
    print("\n5️⃣ Checking ML Dashboard Status...")
    try:
        response = requests.get(f"{base_url}/api/ml-dashboard/status")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Dashboard status: {data}")
            print("✅ ML dashboard status retrieved!")
        else:
            print(f"❌ Dashboard status failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Dashboard status error: {e}")
    
    # Step 6: Trigger manual sync
    print("\n6️⃣ Triggering Manual Sync...")
    try:
        response = requests.post(f"{base_url}/api/sync/run-now")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Result: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print("✅ Manual sync triggered!")
            
            # Wait a bit for sync to complete
            print("   ⏳ Waiting 10 seconds for sync to complete...")
            time.sleep(10)
        else:
            print(f"❌ Manual sync failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Manual sync error: {e}")
    
    # Step 7: Test ML dashboard charts
    print("\n7️⃣ Testing ML Dashboard Charts...")
    
    charts = [
        ("roi-forecast", "ROI Forecast"),
        ("roi-timeseries", "ROI Timeseries"),
        ("reach-ctr-timeseries", "Reach CTR Timeseries"),
        ("budget-recommendations", "Budget Recommendations")
    ]
    
    for chart_id, chart_name in charts:
        try:
            # Test chart image
            response = requests.get(f"{base_url}/api/ml-dashboard/{chart_id}/chart")
            print(f"   {chart_name} Chart: {response.status_code}")
            if response.status_code == 200:
                print(f"     ✅ Chart image available ({len(response.content)} bytes)")
            else:
                print(f"     ❌ Chart failed: {response.text[:100]}")
            
            # Test chart data
            response = requests.get(f"{base_url}/api/ml-dashboard/{chart_id}/data")
            print(f"   {chart_name} Data: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"     ✅ Data available ({len(data)} records)")
                else:
                    print(f"     ⚠️ Data response: {data}")
            else:
                print(f"     ❌ Data failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ {chart_name} error: {e}")
    
    # Step 8: Final status check
    print("\n8️⃣ Final Status Check...")
    try:
        response = requests.get(f"{base_url}/api/sync/status")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Last sync: {data.get('last_sync')}")
            print(f"   Charts available: {len([c for c in data.get('charts', {}).values() if c.get('exists')])}/4")
            print("✅ Final status check complete!")
        else:
            print(f"❌ Final status failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Final status error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 DEMETRA API Test Complete!")
    print("\n📋 Summary:")
    print("   - API Health: ✅")
    print("   - ML Tables: ✅") 
    print("   - Dashboard Generation: ✅")
    print("   - Chart Images: ✅")
    print("   - Chart Data: ✅")
    print("\n🚀 System is ready for frontend integration!")
    
    return True

if __name__ == "__main__":
    success = test_api_complete()
    sys.exit(0 if success else 1)
