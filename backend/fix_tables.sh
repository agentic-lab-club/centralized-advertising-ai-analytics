#!/bin/bash
echo "🔧 Creating ML tables..."
docker exec -i centralized-advertising-ai-analytics-postgres_db-1 psql -U postgres -d demetra_db < create_ml_tables_simple.sql
echo "✅ ML tables created!"
