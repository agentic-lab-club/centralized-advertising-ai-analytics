#!/bin/bash

echo "🚀 DEMETRA SYSTEMS - Curl Test Script"
echo "====================================="

BASE_URL="http://localhost:8000"

# Test 1: Health Check
echo ""
echo "1️⃣ Testing API Health..."
curl -s "$BASE_URL/health" | jq '.' || echo "❌ Health check failed"

# Test 2: Root endpoint
echo ""
echo "2️⃣ Testing Root Endpoint..."
curl -s "$BASE_URL/" | jq '.message, .version' || echo "❌ Root endpoint failed"

# Test 3: Check ML tables
echo ""
echo "3️⃣ Checking ML Tables..."
curl -s "$BASE_URL/api/setup/check-tables" | jq '.' || echo "❌ Check tables failed"

# Test 4: Create ML tables
echo ""
echo "4️⃣ Creating ML Tables..."
curl -s -X POST "$BASE_URL/api/setup/create-ml-tables" | jq '.' || echo "❌ Create tables failed"

# Test 5: ML Dashboard Status
echo ""
echo "5️⃣ ML Dashboard Status..."
curl -s "$BASE_URL/api/ml-dashboard/status" | jq '.' || echo "❌ Dashboard status failed"

# Test 6: Trigger Manual Sync
echo ""
echo "6️⃣ Triggering Manual Sync..."
curl -s -X POST "$BASE_URL/api/sync/run-now" | jq '.' || echo "❌ Manual sync failed"

# Wait for sync
echo ""
echo "⏳ Waiting 10 seconds for sync to complete..."
sleep 10

# Test 7: Test Charts
echo ""
echo "7️⃣ Testing Charts..."

echo "   ROI Forecast Chart:"
curl -s -I "$BASE_URL/api/ml-dashboard/roi-forecast/chart" | head -1

echo "   ROI Forecast Data:"
curl -s "$BASE_URL/api/ml-dashboard/roi-forecast/data" | jq 'length' || echo "No data"

echo "   Budget Recommendations Chart:"
curl -s -I "$BASE_URL/api/ml-dashboard/budget-recommendations/chart" | head -1

echo "   Budget Recommendations Data:"
curl -s "$BASE_URL/api/ml-dashboard/budget-recommendations/data" | jq 'length' || echo "No data"

# Test 8: Final Status
echo ""
echo "8️⃣ Final Sync Status..."
curl -s "$BASE_URL/api/sync/status" | jq '.last_sync, .charts' || echo "❌ Sync status failed"

echo ""
echo "🎉 Curl tests complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Check if all tests passed"
echo "   2. Open http://localhost:3000 for frontend"
echo "   3. Click 'ML Dashboards' tab"
echo "   4. Click 'Manual Sync' button"
