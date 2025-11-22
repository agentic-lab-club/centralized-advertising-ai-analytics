# 🚀 DEMETRA SYSTEMS - Quick Test Guide

## 🔧 **STEP 1: Rebuild & Start Backend**

```bash
cd backend

# Rebuild Docker containers
make build

# Start services
make up

# Check logs
make logs
```

## 🧪 **STEP 2: Run Automated Tests**

### **Option A: Python Test Script**
```bash
cd backend
python test_complete_system.py
```

### **Option B: Curl Test Script**
```bash
cd backend
./test_curl.sh
```

### **Option C: Manual Curl Commands**
```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Create ML tables
curl -X POST http://localhost:8000/api/setup/create-ml-tables

# 3. Check tables
curl http://localhost:8000/api/setup/check-tables

# 4. Trigger ML dashboard generation
curl -X POST http://localhost:8000/api/sync/run-now

# 5. Check dashboard status
curl http://localhost:8000/api/ml-dashboard/status

# 6. Test ROI forecast chart
curl -I http://localhost:8000/api/ml-dashboard/roi-forecast/chart

# 7. Test ROI forecast data
curl http://localhost:8000/api/ml-dashboard/roi-forecast/data
```

## 🎯 **STEP 3: Expected Results**

### **✅ Success Indicators:**
- Health check returns `{"status": "healthy"}`
- ML tables creation returns `{"status": "success"}`
- Manual sync returns `{"status": "success"}`
- Chart endpoints return `200 OK` with PNG data
- Data endpoints return JSON arrays with prediction data

### **❌ Common Issues & Fixes:**

#### **Issue 1: Import Errors**
```
ImportError: cannot import name 'ml_sync_service'
```
**Fix:** I've simplified main.py to remove problematic imports

#### **Issue 2: Missing ML Tables**
```
relation "ml_roi_forecast" does not exist
```
**Fix:** Run `curl -X POST http://localhost:8000/api/setup/create-ml-tables`

#### **Issue 3: Charts Not Generated**
```
Chart "roi_forecast_by_channel" not found
```
**Fix:** Run `curl -X POST http://localhost:8000/api/sync/run-now`

## 🚀 **STEP 4: Test Frontend**

```bash
cd frontend
npm start
```

Then:
1. Open http://localhost:3000
2. Click "🧠 ML Dashboards" tab
3. Click "🚀 Manual Sync" button
4. Wait for charts to load

## 📊 **STEP 5: Verify ML Dashboards**

You should see 4 dashboard cards:
- 📈 ROI Forecast by Channel
- 📊 ROI & Conversion Timeseries  
- 🎯 Reach & CTR Timeseries
- 💰 Budget Recommendations

Each card should show:
- ✅ Status: Ready
- 🖼️ Chart image (PNG)
- 📋 Prediction data table

## 🔍 **Debug Commands**

If something fails:

```bash
# Check backend logs
make logs

# Check if containers are running
docker ps

# Test individual endpoints
curl -v http://localhost:8000/health
curl -v http://localhost:8000/api/setup/check-tables

# Check database connection
docker exec -it postgres_db psql -U postgres -d demetra_db -c "\dt"
```

## 🎉 **Success Criteria**

✅ Backend starts without errors
✅ ML tables are created
✅ Charts generate successfully  
✅ Frontend displays ML dashboards
✅ Manual sync works
✅ All 4 dashboard types show data

---

**🚀 Once all tests pass, your DEMETRA SYSTEMS AI Analytics Dashboard is ready for the hackathon demo!**
