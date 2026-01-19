#!/bin/bash

echo "========================================"
echo "Track Lights Controller - Frontend"
echo "========================================"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo ""
fi

echo "🚀 Starting development server..."
echo ""
echo "Access the app at:"
echo "  - Local:   http://localhost:5173"
echo "  - Network: http://192.168.1.99:5173"
echo ""
echo "Make sure the backend API is running on:"
echo "  http://192.168.1.99:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

npm run dev
