#!/usr/bin/env python3
"""
Test Fixed ML Dashboard System
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url)
        
        print(f"{method} {endpoint}: {response.status_code}")
        if response.status_code == expected_status:
            print(f"  ✅ Success")
            return True
        else:
            print(f"  ❌ Error: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False

def main():
    print("🔧 TESTING FIXED ML DASHBOARD SYSTEM")
    print("=" * 40)
    
    # Basic health checks
    print("\n1. Basic Health Checks:")
    test_endpoint("GET", "/health")
    test_endpoint("GET", "/api/test")
    
    # Generate sample data
    print("\n2. Generate Sample Data:")
    test_endpoint("POST", "/api/sync/generate-sample-data")
    
    # Test ML dashboard endpoints
    print("\n3. ML Dashboard Endpoints:")
    test_endpoint("GET", "/api/ml-dashboard/roi-forecast/chart")
    test_endpoint("GET", "/api/ml-dashboard/roi-forecast/data")
    test_endpoint("GET", "/api/ml-dashboard/status")
    
    print("\n✅ FIXED ML SYSTEM TEST COMPLETE!")

if __name__ == "__main__":
    main()
