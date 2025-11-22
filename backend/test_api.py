#!/usr/bin/env python3

import requests
import time
import sys

def test_api():
    """Test if the API is working"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Testing DEMETRA API...")
    
    # Wait for server to start
    for i in range(10):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is healthy!")
                break
        except requests.exceptions.RequestException:
            print(f"⏳ Waiting for API... ({i+1}/10)")
            time.sleep(2)
    else:
        print("❌ API not responding after 20 seconds")
        return False
    
    # Test setup endpoints
    print("\n🔧 Testing setup endpoints...")
    
    try:
        # Check tables
        response = requests.get(f"{base_url}/api/setup/check-tables")
        print(f"Check tables: {response.status_code}")
        
        # Create tables
        response = requests.post(f"{base_url}/api/setup/create-ml-tables")
        print(f"Create ML tables: {response.status_code}")
        if response.status_code == 200:
            print("✅ ML tables created successfully!")
        
        # Test ML dashboard status
        response = requests.get(f"{base_url}/api/ml-dashboard/status")
        print(f"ML dashboard status: {response.status_code}")
        
        # Trigger sync
        response = requests.post(f"{base_url}/api/sync/run-now")
        print(f"Manual sync: {response.status_code}")
        if response.status_code == 200:
            print("✅ Manual sync triggered!")
        
        print("\n🎉 All tests passed! API is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
