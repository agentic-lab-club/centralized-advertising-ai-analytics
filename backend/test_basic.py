#!/usr/bin/env python3
"""
Test Basic API with Recommendations
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"{method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Success: {json.dumps(result, indent=2)[:200]}...")
        else:
            print(f"  ❌ Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")

def main():
    print("🔧 TESTING API WITH RECOMMENDATIONS")
    print("=" * 40)
    
    # Basic endpoints
    print("\n1. Basic Endpoints:")
    test_endpoint("/")
    test_endpoint("/health")
    test_endpoint("/api/test")
    
    # Recommendations endpoints
    print("\n2. Recommendations Endpoints:")
    test_endpoint("/api/recommendations/analytics")
    test_endpoint("/api/recommendations/channels")
    test_endpoint("/api/recommendations/budget")
    
    # Custom recommendations
    print("\n3. Custom Recommendations:")
    custom_data = {
        "budget": 100000,
        "channels": ["Facebook", "Instagram"],
        "goal": "maximize_roi"
    }
    test_endpoint("/api/recommendations/custom", "POST", custom_data)
    
    print("\n✅ RECOMMENDATIONS API TEST COMPLETE!")

if __name__ == "__main__":
    main()
