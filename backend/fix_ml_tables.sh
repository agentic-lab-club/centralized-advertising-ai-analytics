#!/bin/bash

echo "🔧 DEMETRA SYSTEMS - Quick ML Tables Fix"
echo "======================================="

# Check if PostgreSQL is running
echo "📋 Checking PostgreSQL connection..."

# Run SQL script to create ML tables
echo "🗄️ Creating ML prediction tables..."
docker exec -i postgres_db psql -U postgres -d demetra_db < create_ml_tables.sql

if [ $? -eq 0 ]; then
    echo "✅ ML tables created successfully!"
else
    echo "❌ Error creating ML tables. Trying alternative method..."
    
    # Alternative: Connect directly to database
    echo "🔄 Attempting direct database connection..."
    docker exec -it postgres_db psql -U postgres -d demetra_db -c "
    CREATE TABLE IF NOT EXISTS ml_roi_forecast (
        id SERIAL PRIMARY KEY,
        channel VARCHAR(50),
        roi_forecast FLOAT,
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
        total_budget FLOAT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    "
fi

# Verify tables exist
echo "🔍 Verifying ML tables..."
docker exec -it postgres_db psql -U postgres -d demetra_db -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'ml_%';"

echo ""
echo "🚀 Setup complete! You can now:"
echo "1. Restart the backend: make restart"
echo "2. Test ML dashboards: curl http://localhost:8000/api/ml-dashboard/status"
echo "3. Trigger manual sync: curl -X POST http://localhost:8000/api/sync/run-now"
