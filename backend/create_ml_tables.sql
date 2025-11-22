-- Create ML Prediction Tables for DEMETRA SYSTEMS
-- Run this in PostgreSQL to create the missing tables

-- 1. ROI Forecast Table
CREATE TABLE IF NOT EXISTS ml_roi_forecast (
    id SERIAL PRIMARY KEY,
    channel VARCHAR(50),
    roi_forecast FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_ml_roi_forecast_id ON ml_roi_forecast (id);
CREATE INDEX IF NOT EXISTS ix_ml_roi_forecast_channel ON ml_roi_forecast (channel);

-- 2. ROI Timeseries Table
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

CREATE INDEX IF NOT EXISTS ix_ml_roi_timeseries_id ON ml_roi_timeseries (id);
CREATE INDEX IF NOT EXISTS ix_ml_roi_timeseries_channel ON ml_roi_timeseries (channel);

-- 3. Reach CTR Timeseries Table
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

CREATE INDEX IF NOT EXISTS ix_ml_reach_ctr_timeseries_id ON ml_reach_ctr_timeseries (id);
CREATE INDEX IF NOT EXISTS ix_ml_reach_ctr_timeseries_channel ON ml_reach_ctr_timeseries (channel);

-- 4. Budget Recommendations Table
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

CREATE INDEX IF NOT EXISTS ix_ml_budget_rec_id ON ml_budget_rec (id);
CREATE INDEX IF NOT EXISTS ix_ml_budget_rec_channel ON ml_budget_rec (channel);

-- Verify tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE 'ml_%';
