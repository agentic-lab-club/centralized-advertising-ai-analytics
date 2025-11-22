# 🚀 ML DASHBOARD SYSTEM - QUICK START

## ✨ What's New

Your ML dashboard system now includes:

1. **4 ML Prediction Tables** - Store forecasts for each dashboard type
2. **Seaborn Chart Generation** - PNG charts for frontend consumption  
3. **30-Minute Auto Polling** - APScheduler runs every 30 minutes
4. **Manual Sync API** - Hands-on execution for demos
5. **Complete API Endpoints** - Chart PNGs + JSON data for each dashboard

---

## 🏃‍♂️ QUICK START (3 minutes)

### 1. Start the Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test the System
```bash
python test_ml_complete.py
```

### 3. Generate Sample Data
```bash
curl -X POST http://localhost:8000/api/sync/generate-sample-data
```

### 4. View Dashboards
- ROI Forecast: http://localhost:8000/api/ml-dashboard/roi-forecast/chart
- ROI Timeseries: http://localhost:8000/api/ml-dashboard/roi-timeseries/chart  
- Reach/CTR: http://localhost:8000/api/ml-dashboard/reach-ctr/chart
- Budget Rec: http://localhost:8000/api/ml-dashboard/budget-recommendation/chart

---

## 📊 DASHBOARD ENDPOINTS

### Chart PNGs (for Frontend)
```
GET /api/ml-dashboard/roi-forecast/chart          # ROI forecast by channel
GET /api/ml-dashboard/roi-timeseries/chart        # ROI & conversion over time  
GET /api/ml-dashboard/reach-ctr/chart             # Reach & CTR over time
GET /api/ml-dashboard/budget-recommendation/chart # Budget allocation
```

### Data JSON (for Tables)
```
GET /api/ml-dashboard/roi-forecast/data           # ROI forecast data
GET /api/ml-dashboard/roi-timeseries/data         # Timeseries data
GET /api/ml-dashboard/reach-ctr/data              # Reach/CTR data  
GET /api/ml-dashboard/budget-recommendation/data  # Budget data
```

---

## 🔄 SCHEDULER & SYNC

### Automatic (Every 30 Minutes)
- Scheduler starts automatically with the app
- Updates all 4 ML prediction tables
- Regenerates all PNG charts
- No manual intervention needed

### Manual Sync (Hands-On)
```bash
# Trigger sync manually (for demos)
curl -X POST http://localhost:8000/api/sync/run-now

# Check scheduler status
curl http://localhost:8000/api/sync/status

# Generate all dashboards
curl -X POST http://localhost:8000/api/ml-dashboard/generate-all
```

---

## 🗄️ DATABASE TABLES

The system creates 4 ML prediction tables:

1. **ml_roi_forecast** - ROI forecasts by channel
2. **ml_roi_timeseries** - ROI & conversion over time
3. **ml_reach_ctr_timeseries** - Reach & CTR over time  
4. **ml_budget_rec** - Budget recommendations

---

## 🖼️ FRONTEND INTEGRATION

### React Component Example
```jsx
// Fetch PNG chart
const [chartUrl, setChartUrl] = useState('');

useEffect(() => {
  setChartUrl('http://localhost:8000/api/ml-dashboard/roi-forecast/chart');
}, []);

return <img src={chartUrl} alt="ROI Forecast" />;
```

### Polling Every 30 Minutes
```jsx
useEffect(() => {
  const interval = setInterval(() => {
    // Refresh chart URLs
    setChartUrl(`http://localhost:8000/api/ml-dashboard/roi-forecast/chart?t=${Date.now()}`);
  }, 30 * 60 * 1000); // 30 minutes

  return () => clearInterval(interval);
}, []);
```

---

## 🧪 TESTING

### Complete System Test
```bash
python test_ml_complete.py
```

### Individual Tests
```bash
# Test chart generation
curl http://localhost:8000/api/ml-dashboard/roi-forecast/chart

# Test data endpoints  
curl http://localhost:8000/api/ml-dashboard/roi-forecast/data

# Test manual sync
curl -X POST http://localhost:8000/api/sync/run-now
```

---

## 🎯 PRODUCTION CHECKLIST

- [x] 4 ML prediction tables created
- [x] Seaborn chart generation working
- [x] 30-minute scheduler running
- [x] Manual sync API available
- [x] PNG + JSON endpoints ready
- [x] Frontend integration tested
- [x] Error handling implemented
- [x] Logging configured

---

## 🚨 TROUBLESHOOTING

### Charts Not Generating?
```bash
# Check static directory exists
ls -la backend/static/

# Check scheduler status
curl http://localhost:8000/api/sync/status
```

### Database Issues?
```bash
# Check tables exist
curl http://localhost:8000/api/setup/check-tables

# Recreate tables
curl -X POST http://localhost:8000/api/setup/create-ml-tables
```

### Scheduler Not Running?
```bash
# Check app logs for scheduler startup
# Manually start scheduler
curl -X POST http://localhost:8000/api/sync/start-scheduler
```

---

**🎉 Your ML Dashboard System is Ready for Production!**

The system now automatically generates ML predictions every 30 minutes and serves them as PNG charts and JSON data for your frontend to consume.
