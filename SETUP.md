# AI House Price Predictor

Complete full-stack application for predicting house prices in Delhi using Machine Learning.

## 🏗️ Project Structure

```
house-price-prediction/
├── backend/
│   ├── app.py              # Flask API
│   ├── model.pkl           # Trained ML model
│   ├── requirements.txt     # Backend dependencies
│   └── .env               # Environment variables
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css
│   │   ├── index.jsx
│   │   └── index.css
│   ├── package.json
│   └── .env
├── Delhi_house_data.csv    # Training dataset
└── README.md
```

## 🚀 Setup & Installation

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend will run on: `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on: `http://localhost:3000`

## 📋 Features

- **Beautiful UI**: Modern, responsive design with Tailwind CSS
- **Real-time Predictions**: Instant house price predictions
- **Multiple Parameters**: Area, BHK, Bathrooms, Locality, Furnishing, etc.
- **Professional Design**: Gradient backgrounds, smooth animations
- **Error Handling**: Comprehensive error messages

## 🔧 Available Endpoints

### GET `/api/options`
Returns all available options for dropdowns

### POST `/api/predict`
Make a price prediction

**Request Body:**
```json
{
  "area": 1200,
  "bhk": 3,
  "bathroom": 2,
  "furnishing": "Semi-Furnished",
  "locality": "Rohini Sector 24",
  "parking": 1,
  "status": "Ready_to_move",
  "transaction": "New_Property",
  "property_type": "Apartment"
}
```

**Response:**
```json
{
  "success": true,
  "predicted_price": 7500000.50,
  "currency": "₹",
  "message": "Predicted house price: ₹ 7,500,000.50"
}
```

## 📊 Model Details

- **Algorithm**: Linear Regression
- **Features**: Area, BHK, Bathroom, Furnishing, Locality, Parking, Status, Transaction, Type, Per_Sqft, TotalRooms
- **Target**: House Price in INR
- **Preprocessing**: OneHotEncoder for categorical features

## 🎨 UI Features

- ✅ Responsive design (mobile & desktop)
- ✅ Gradient backgrounds
- ✅ Smooth transitions & animations
- ✅ Clear input validation
- ✅ Loading states
- ✅ Error messages
- ✅ Formatted price display

## 🤝 How It Works

1. User enters property details
2. Frontend sends data to Flask backend
3. Backend loads the trained model
4. Model preprocesses the input
5. Prediction is calculated
6. Result is returned to frontend
7. Frontend displays the predicted price

## 🛠️ Technologies Used

**Frontend:**
- React 18
- Axios (for API calls)
- Tailwind CSS (styling)

**Backend:**
- Flask
- Flask-CORS
- Scikit-learn
- Pandas
- NumPy
- Joblib

## 📝 Notes

- Make sure both backend and frontend are running
- Backend must be running before frontend
- CORS is enabled for cross-origin requests
- Model uses OneHotEncoder for categorical features

## ⚙️ Environment Variables

Create `.env` files in both frontend and backend directories if needed.

**Backend .env:**
```
FLASK_ENV=development
FLASK_DEBUG=True
```

**Frontend .env:**
```
REACT_APP_API_URL=http://localhost:5000
```

---

🔥 **Ready to predict house prices!**
