# 🔧 MANUAL SQL FIX - DEMETRA SYSTEMS

## 🚨 **URGENT: Run these SQL commands to fix the database**

### **Step 1: Connect to PostgreSQL**

Since Docker commands aren't working in your environment, you need to connect to PostgreSQL manually and run these commands:

### **Step 2: Run these SQL commands**

```sql
-- Connect to your PostgreSQL database and run these commands:

-- 1. Create ml_roi_forecast table
CREATE TABLE IF NOT EXISTS ml_roi_forecast (
    id SERIAL PRIMARY KEY,
    channel VARCHAR(50),
    roi_forecast FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create ml_roi_timeseries table
CREATE TABLE IF NOT EXISTS ml_roi_timeseries (
    id SERIAL PRIMARY KEY,
    date DATE,
    channel VARCHAR(50),
    roi_actual FLOAT,
    conversion_actual FLOAT,
    roi_pred FLOAT,
    conversion_pred FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create ml_reach_ctr_timeseries table
CREATE TABLE IF NOT EXISTS ml_reach_ctr_timeseries (
    id SERIAL PRIMARY KEY,
    date DATE,
    channel VARCHAR(50),
    reach_actual INTEGER,
    ctr_actual FLOAT,
    reach_pred INTEGER,
    ctr_pred FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create ml_budget_rec table
CREATE TABLE IF NOT EXISTS ml_budget_rec (
    id SERIAL PRIMARY KEY,
    channel VARCHAR(50),
    roi_pred FLOAT,
    conversion_pred FLOAT,
    acquisition_cost FLOAT,
    recommended_budget FLOAT,
    total_budget FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Verify tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE 'ml_%';
```

### **Step 3: How to Connect**

**Option A: Using pgAdmin or any PostgreSQL client:**
- Host: localhost
- Port: 5432
- Database: demetra_db
- Username: postgres
- Password: (your postgres password)

**Option B: Using command line (if available):**
```bash
psql -h localhost -p 5432 -U postgres -d demetra_db
```

**Option C: Using Docker Desktop GUI:**
1. Open Docker Desktop
2. Go to Containers
3. Find `postgres_db` container
4. Click "Exec" tab
5. Run: `psql -U postgres -d demetra_db`
6. Paste the SQL commands above

### **Step 4: Restart Backend**

After creating the tables:
```bash
cd backend
make restart
```

### **Step 5: Test**

```bash
# Test API
curl http://localhost:8000/api/ml-dashboard/status

# Trigger sync
curl -X POST http://localhost:8000/api/sync/run-now
```

## 🎯 **What This Fixes:**

1. ✅ Creates missing ML prediction tables
2. ✅ Fixes "relation does not exist" errors
3. ✅ Enables ML dashboard generation
4. ✅ Allows frontend to display charts

## 🚨 **CRITICAL: Do this NOW**

The backend is failing because these tables don't exist. Once you create them, everything will work perfectly!
