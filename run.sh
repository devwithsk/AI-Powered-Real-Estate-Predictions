#!/bin/bash

echo ""
echo "============================================"
echo " House Price Prediction - Full Stack App"
echo "============================================"
echo ""

echo "[Step 1] Installing/Updating backend dependencies..."
cd backend
pip install -r requirements.txt
echo "✅ Backend dependencies installed"
echo ""

echo "[Step 2] Installing/Updating frontend dependencies..."
cd ../frontend
npm install
echo "✅ Frontend dependencies installed"
echo ""

echo ""
echo "============================================"
echo " Starting Application..."
echo "============================================"
echo ""
echo "Backend will run on: http://localhost:5000"
echo "Frontend will run on: http://localhost:3000"
echo ""

cd ..

# Start backend in background
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
cd frontend
npm start
cd ..

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT

wait
