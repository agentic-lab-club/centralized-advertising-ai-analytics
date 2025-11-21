#!/bin/bash

echo "🚀 Starting DEMETRA SYSTEMS Frontend Dashboard"
echo "=============================================="

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
fi

echo "🌐 Starting development server..."
echo "Dashboard will be available at: http://localhost:3000"
echo "Backend API should be running at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"

npm start
