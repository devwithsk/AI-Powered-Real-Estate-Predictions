# 🚀 Quick Start Guide

## ⚡ Fastest Way to Run (Recommended)

### On Windows:
```bash
cd e:\AI Projects\house-price-prediction
run.bat
```

That's it! Both backend and frontend will start automatically.

---

## Manual Setup (If run.bat doesn't work)

### Step 1: Install Backend Dependencies

```bash
cd "e:\AI Projects\house-price-prediction\backend"
pip install -r requirements.txt
```

### Step 2: Start Backend Server

```bash
cd "e:\AI Projects\house-price-prediction\backend"
python app.py
```

✅ Backend will run on: **http://localhost:5000**

### Step 3: Install Frontend Dependencies (New Terminal/CMD)

```bash
cd "e:\AI Projects\house-price-prediction\frontend"
npm install
```

### Step 4: Start Frontend App

```bash
npm start
```

✅ Frontend will open automatically at: **http://localhost:3000**

---

## 🧪 Test It Out

1. Open http://localhost:3000 in your browser
2. Fill in the form:
   - Area: 1500
   - BHK: 3
   - Bathrooms: 2
   - Locality: Rohini Sector 24
   - Furnishing: Semi-Furnished
   - Parking: 1
   - Status: Ready to move
   - Type: Apartment
   - Transaction: New Property

3. Click "🔮 Predict Price"
4. See your predicted house price! 🎉

---

## 📋 Prerequisites

Make sure you have:
- **Python 3.7+** - [Download](https://www.python.org/downloads/)
- **Node.js & npm** - [Download](https://nodejs.org/)
- **Git** (optional) - [Download](https://git-scm.com/)

Check versions:
```bash
python --version
npm --version
```

---

## 🆘 If Something Goes Wrong

### Issue: "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue: "Port 3000 already in use"
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :3000
kill -9 <PID>
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "npm ERR! code ENOENT"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Issue: Backend not connecting
- Make sure backend is running on http://localhost:5000
- Check firewall settings
- Try restarting both services

---

## 📚 What Each File Does

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask API server - handles predictions |
| `backend/model.pkl` | Trained ML model - does the predictions |
| `frontend/App.jsx` | Main React component - user interface |
| `run.bat` | Starts both services (Windows) |
| `run.sh` | Starts both services (Linux/Mac) |
| `Delhi_house_data.csv` | Training data used for the model |
| `main.py` | Original model training script |

---

## 🎯 Key Features

✅ Real-time predictions
✅ Beautiful, responsive UI
✅ Multiple parameters
✅ Error handling
✅ Professional design
✅ Works offline (once started)

---

## 🔗 Useful URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Docs: http://localhost:5000/api/options
- Health Check: http://localhost:5000/health

---

## 💡 Tips

1. **Keep both windows open** - Backend and Frontend both need to run
2. **Check console errors** - Look at terminal output for debugging
3. **Refresh browser** - If frontend looks broken, refresh the page
4. **Wait for startup** - Give apps 5-10 seconds to fully load
5. **Model takes time** - First prediction might be slower

---

## 🎉 You're All Set!

Your AI House Price Predictor is ready to go! 

**Next Step:** Run `run.bat` (Windows) or `./run.sh` (Linux/Mac) and open http://localhost:3000

---

Happy predicting! 🏠💰
