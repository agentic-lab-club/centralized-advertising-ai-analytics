-- Create ML tables
CREATE TABLE IF NOT EXISTS ml_roi_forecast (
    id SERIAL PRIMARY KEY,
    channel VARCHAR(50),
    roi_forecast FLOAT,
    confidence_score FLOAT DEFAULT 0.85,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS ml_budget_rec (
    id SERIAL PRIMARY KEY,
    channel VARCHAR(50),
    roi_pred FLOAT,
    conversion_pred FLOAT,
    acquisition_cost FLOAT,
    recommended_budget FLOAT,
    total_budget FLOAT DEFAULT 100000.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample data
INSERT INTO ml_roi_forecast (channel, roi_forecast, confidence_score) VALUES
('Facebook', 3.2, 0.85),
('Instagram', 2.8, 0.90),
('Twitter', 2.5, 0.80),
('Pinterest', 1.8, 0.75);

INSERT INTO ml_budget_rec (channel, roi_pred, conversion_pred, acquisition_cost, recommended_budget) VALUES
('Facebook', 3.2, 0.08, 7500, 35000),
('Instagram', 2.8, 0.09, 7200, 30000),
('Twitter', 2.5, 0.07, 8000, 25000),
('Pinterest', 1.8, 0.06, 8500, 10000);
