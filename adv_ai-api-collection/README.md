# 🚀 DEMETRA AI Analytics - Bruno API Collection

## 📁 Collection Structure

### 01 - Health & Status
- **Health Check** - `GET /health`
- **API Test** - `GET /api/test`

### 02 - ML Dashboards
- **ROI Forecast Chart** - `GET /api/ml-dashboard/roi-forecast/chart` (PNG)
- **ROI Forecast Data** - `GET /api/ml-dashboard/roi-forecast/data` (JSON)
- **ROI Timeseries Chart** - `GET /api/ml-dashboard/roi-timeseries/chart` (PNG)
- **ROI Timeseries Data** - `GET /api/ml-dashboard/roi-timeseries/data` (JSON)
- **Reach CTR Chart** - `GET /api/ml-dashboard/reach-ctr/chart` (PNG)
- **Reach CTR Data** - `GET /api/ml-dashboard/reach-ctr/data` (JSON)
- **Budget Recommendation Chart** - `GET /api/ml-dashboard/budget-recommendation/chart` (PNG)
- **Budget Recommendation Data** - `GET /api/ml-dashboard/budget-recommendation/data` (JSON)
- **Dashboard Status** - `GET /api/ml-dashboard/status`
- **Generate All Dashboards** - `POST /api/ml-dashboard/generate-all`

### 03 - Scheduler & Sync
- **Sync Now (Manual)** - `POST /api/sync/run-now`
- **Sync Status** - `GET /api/sync/status`
- **Start Scheduler** - `POST /api/sync/start-scheduler`
- **Stop Scheduler** - `POST /api/sync/stop-scheduler`

### 04 - Mock Data
- **Generate Sample Data** - `POST /api/sync/generate-sample-data`
- **Mock All Data** - `POST /api/test/mock-all`

### 05 - Recommendations
- **AI Analytics** - `GET /api/recommendations/analytics`
- **Channel Performance** - `GET /api/recommendations/channels`
- **Budget Allocation** - `GET /api/recommendations/budget`
- **Custom Recommendations** - `POST /api/recommendations/custom`

## 🎯 Quick Test Sequence

1. **Health Check** → Verify API is running
2. **AI Analytics** → Get AI recommendations
3. **Channel Performance** → View channel data
4. **Budget Allocation** → Get budget suggestions
5. **Custom Recommendations** → Send custom data for analysis

## 🔧 Environment Variables

- `baseUrl`: http://localhost:8000

## 🤖 AI Recommendations

The recommendations endpoints provide:
- Channel performance analysis
- Budget optimization suggestions
- ROI improvement strategies
- Custom analytics based on user data

## 📊 Chart Endpoints (PNG)

All chart endpoints return PNG images that can be displayed directly in frontend:

- ROI Forecast by Channel
- ROI & Conversion Over Time  
- Reach & CTR Over Time
- Budget Recommendations

## 🔄 Scheduler (30min Auto-Sync)

The scheduler runs automatically every 30 minutes. Use manual sync for demos and testing.
