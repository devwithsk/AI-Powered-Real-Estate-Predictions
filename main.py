"""
House Price Prediction - Quick Test Script
This script tests the trained model with sample data.

For training/retraining the model, run: python train_model.py
"""

import pandas as pd
import numpy as np
import joblib
import os

print("=" * 60)
print("HOUSE PRICE PREDICTION - MODEL TEST")
print("=" * 60)

# =========================================
# LOAD MODEL
# =========================================
print("\n[1/3] Loading trained model...")

MODEL_PATH = os.path.join('backend', 'model.pkl')

if not os.path.exists(MODEL_PATH):
    print(f"✗ Error: Model not found at {MODEL_PATH}")
    print("Please run 'python train_model.py' to train the model first.")
    exit(1)

try:
    model = joblib.load(MODEL_PATH)
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    exit(1)

# =========================================
# LOAD METADATA
# =========================================
print("\n[2/3] Loading model metadata...")

METADATA_PATH = os.path.join('backend', 'model_metadata.json')

if os.path.exists(METADATA_PATH):
    import json
    with open(METADATA_PATH, 'r') as f:
        metadata = json.load(f)
    
    print("✓ Model Metadata:")
    print(f"  - Created: {metadata['timestamp']}")
    print(f"  - Test R² Score: {metadata['test_r2']:.4f}")
    print(f"  - Test MAE: ₹ {metadata['test_mae']:,.2f}")
    print(f"  - Training Samples: {metadata['training_samples']}")
else:
    print("✗ Metadata file not found (expected after training)")

# =========================================
# TEST PREDICTION
# =========================================
print("\n[3/3] Making sample predictions...\n")

# Example 1: Budget 2 BHK in Dwarka
sample_house_1 = pd.DataFrame({
    "Area": [1200],
    "BHK": [2],
    "Bathroom": [2],
    "Furnishing": ["Semi-Furnished"],
    "Locality": ["Dwarka Sector 12"],
    "Parking": [1],
    "Status": ["Ready_to_move"],
    "Transaction": ["New_Property"],
    "Type": ["Apartment"],
    "Per_Sqft": [5000]
})
sample_house_1["TotalRooms"] = sample_house_1["BHK"] + sample_house_1["Bathroom"]

# Example 2: Luxury 3 BHK in Indirapuram
sample_house_2 = pd.DataFrame({
    "Area": [1800],
    "BHK": [3],
    "Bathroom": [3],
    "Furnishing": ["Furnished"],
    "Locality": ["Indirapuram"],
    "Parking": [2],
    "Status": ["Ready_to_move"],
    "Transaction": ["Resale"],
    "Type": ["Villa"],
    "Per_Sqft": [5000]
})
sample_house_2["TotalRooms"] = sample_house_2["BHK"] + sample_house_2["Bathroom"]

# Example 3: Under construction 4 BHK in Sector 62
sample_house_3 = pd.DataFrame({
    "Area": [2400],
    "BHK": [4],
    "Bathroom": [3],
    "Furnishing": ["Unfurnished"],
    "Locality": ["Sector 62"],
    "Parking": [3],
    "Status": ["Under_Construction"],
    "Transaction": ["New_Property"],
    "Type": ["Independent_House"],
    "Per_Sqft": [5000]
})
sample_house_3["TotalRooms"] = sample_house_3["BHK"] + sample_house_3["Bathroom"]

# Make predictions
print("Example 1: Budget Apartment in Dwarka")
print("-" * 60)
pred_1 = model.predict(sample_house_1)[0]
print(f"Area: {sample_house_1['Area'].values[0]} sq ft")
print(f"Configuration: {sample_house_1['BHK'].values[0]} BHK, {sample_house_1['Bathroom'].values[0]} Bathrooms")
print(f"Location: {sample_house_1['Locality'].values[0]}")
print(f"Furnishing: {sample_house_1['Furnishing'].values[0]}")
print(f"Predicted Price: ₹ {pred_1:,.2f}")
print(f"Price Range: ₹ {pred_1*0.9:,.2f} - ₹ {pred_1*1.1:,.2f}\n")

print("Example 2: Luxury Villa in Indirapuram")
print("-" * 60)
pred_2 = model.predict(sample_house_2)[0]
print(f"Area: {sample_house_2['Area'].values[0]} sq ft")
print(f"Configuration: {sample_house_2['BHK'].values[0]} BHK, {sample_house_2['Bathroom'].values[0]} Bathrooms")
print(f"Location: {sample_house_2['Locality'].values[0]}")
print(f"Furnishing: {sample_house_2['Furnishing'].values[0]}")
print(f"Predicted Price: ₹ {pred_2:,.2f}")
print(f"Price Range: ₹ {pred_2*0.9:,.2f} - ₹ {pred_2*1.1:,.2f}\n")

print("Example 3: Under Construction Independent House")
print("-" * 60)
pred_3 = model.predict(sample_house_3)[0]
print(f"Area: {sample_house_3['Area'].values[0]} sq ft")
print(f"Configuration: {sample_house_3['BHK'].values[0]} BHK, {sample_house_3['Bathroom'].values[0]} Bathrooms")
print(f"Location: {sample_house_3['Locality'].values[0]}")
print(f"Furnishing: {sample_house_3['Furnishing'].values[0]}")
print(f"Predicted Price: ₹ {pred_3:,.2f}")
print(f"Price Range: ₹ {pred_3*0.9:,.2f} - ₹ {pred_3*1.1:,.2f}\n")

print("=" * 60)
print("✓ TEST COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nTo train/retrain the model, run: python train_model.py")
print("To start the API server, run: python backend/app.py")
