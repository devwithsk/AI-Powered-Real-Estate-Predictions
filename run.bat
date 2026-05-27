@echo off
echo.
echo ============================================
echo  House Price Prediction - Full Stack App
echo ============================================
echo.

echo [Step 1] Installing/Updating backend dependencies...
cd backend
pip install -r requirements.txt
echo ✅ Backend dependencies installed
echo.

echo [Step 2] Installing/Updating frontend dependencies...
cd ..\frontend
call npm install
echo ✅ Frontend dependencies installed
echo.

echo.
echo ============================================
echo  Starting Application...
echo ============================================
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:3000
echo.

cd ..

REM Start backend in a new window
start "Backend - Flask Server" cmd /k "cd backend && python app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in a new window
start "Frontend - React App" cmd /k "cd frontend && npm start"

echo.
echo ✅ Both services are starting...
echo Please wait for both windows to fully load.
echo.
