"""
Train ML Model for House Price Prediction
This script trains a RandomForest model on Delhi housing data
Run this script to train/retrain the model
"""

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# Machine Learning Libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Encoding
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

print("=" * 60)
print("HOUSE PRICE PREDICTION MODEL TRAINING")
print("=" * 60)

# =========================================
# STEP 1 — LOAD DATASET
# =========================================
print("\n[1/12] Loading dataset...")
try:
    df = pd.read_csv("Delhi_house_data.csv")
    print(f"✓ Dataset loaded successfully!")
    print(f"✓ Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
except FileNotFoundError:
    print("✗ Error: Delhi_house_data.csv not found!")
    exit(1)

# Display dataset info
print("Dataset Preview:")
print(df.head())
print()

# =========================================
# STEP 2 — HANDLE MISSING VALUES
# =========================================
print("[2/12] Handling missing values...")

# Numerical columns
numerical_columns = ["Area", "BHK", "Bathroom", "Parking"]
print(f"  Numerical columns: {numerical_columns}")

# Fill numerical missing values with mean
num_imputer = SimpleImputer(strategy="mean")
df[numerical_columns] = num_imputer.fit_transform(df[numerical_columns])
print(f"  ✓ Imputed {len(numerical_columns)} numerical columns with mean")

# Categorical columns
categorical_fill_columns = ["Furnishing", "Locality", "Status", "Transaction", "Type"]
print(f"  Categorical columns: {categorical_fill_columns}")

# Fill categorical missing values with most frequent value
cat_imputer = SimpleImputer(strategy="most_frequent")
df[categorical_fill_columns] = cat_imputer.fit_transform(df[categorical_fill_columns])
print(f"  ✓ Imputed {len(categorical_fill_columns)} categorical columns with mode\n")

# =========================================
# STEP 3 — FEATURE ENGINEERING
# =========================================
print("[3/12] Feature engineering...")

# Total rooms feature
df["TotalRooms"] = df["BHK"] + df["Bathroom"]
print("  ✓ Created TotalRooms feature (BHK + Bathroom)\n")

# =========================================
# STEP 4 — HANDLE Per_Sqft MISSING VALUES
# =========================================
print("[4/12] Handling Per_Sqft missing values...")
df["Per_Sqft"] = df["Per_Sqft"].fillna(df["Per_Sqft"].median())
print(f"  ✓ Filled Per_Sqft missing values with median\n")

# =========================================
# STEP 5 — REMOVE OUTLIERS USING IQR
# =========================================
print("[5/12] Removing outliers using IQR method...")
Q1 = df["Price"].quantile(0.25)
Q3 = df["Price"].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

initial_count = len(df)
df = df[(df["Price"] >= lower_limit) & (df["Price"] <= upper_limit)]
removed_count = initial_count - len(df)

print(f"  ✓ Removed {removed_count} outliers")
print(f"  ✓ Remaining rows: {len(df)}\n")

# =========================================
# STEP 6 — PREPARE FEATURES & TARGET
# =========================================
print("[6/12] Preparing features and target...")

X = df.drop("Price", axis=1)
y = df["Price"]

print(f"  ✓ Features shape: {X.shape}")
print(f"  ✓ Target shape: {y.shape}\n")

# =========================================
# STEP 7 — IDENTIFY CATEGORICAL COLUMNS
# =========================================
print("[7/12] Identifying categorical columns...")

categorical_columns = ["Furnishing", "Locality", "Status", "Transaction", "Type"]
print(f"  ✓ Categorical columns: {categorical_columns}\n")

# =========================================
# STEP 8 — CREATE PREPROCESSING PIPELINE
# =========================================
print("[8/12] Creating preprocessing pipeline...")

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            categorical_columns
        )
    ],
    remainder="passthrough"
)
print("  ✓ Preprocessing pipeline created\n")

# =========================================
# STEP 9 — CREATE ML PIPELINE
# =========================================
print("[9/12] Creating machine learning pipeline...")

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        max_depth=20,
        min_samples_split=5,
        verbose=0
    ))
])
print("  ✓ ML Pipeline created")
print("  ✓ Model: RandomForestRegressor")
print("  ✓ Parameters: n_estimators=200, max_depth=20, min_samples_split=5\n")

# =========================================
# STEP 10 — TRAIN TEST SPLIT
# =========================================
print("[10/12] Splitting data into train/test sets...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"  ✓ Training set size: {len(X_train)} ({int((len(X_train)/len(X))*100)}%)")
print(f"  ✓ Test set size: {len(X_test)} ({int((len(X_test)/len(X))*100)}%)\n")

# =========================================
# STEP 11 — TRAIN MODEL
# =========================================
print("[11/12] Training model...")
model.fit(X_train, y_train)
print("  ✓ Model training completed!\n")

# =========================================
# STEP 12 — MODEL EVALUATION
# =========================================
print("[12/12] Evaluating model performance...\n")

# Predictions
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

# Metrics
train_mae = mean_absolute_error(y_train, train_predictions)
test_mae = mean_absolute_error(y_test, test_predictions)

train_rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))

train_r2 = r2_score(y_train, train_predictions)
test_r2 = r2_score(y_test, test_predictions)

print("=" * 60)
print("MODEL PERFORMANCE METRICS")
print("=" * 60)
print(f"\n{'Metric':<20} {'Training':<20} {'Testing':<20}")
print("-" * 60)
print(f"{'MAE':<20} {'₹ {:,.2f}'.format(train_mae):<20} {'₹ {:,.2f}'.format(test_mae):<20}")
print(f"{'RMSE':<20} {'₹ {:,.2f}'.format(train_rmse):<20} {'₹ {:,.2f}'.format(test_rmse):<20}")
print(f"{'R² Score':<20} {train_r2:.4f}{'':<14} {test_r2:.4f}")
print("-" * 60)

# Sample predictions
print("\nSample Predictions (Test Set):")
print(f"{'#':<3} {'Predicted':<20} {'Actual':<20} {'Error':<15}")
print("-" * 60)
for i in range(min(5, len(y_test))):
    error = abs(test_predictions[i] - y_test.iloc[i])
    error_pct = (error / y_test.iloc[i]) * 100
    print(f"{i+1:<3} {'₹ {:,.2f}'.format(test_predictions[i]):<20} {'₹ {:,.2f}'.format(y_test.iloc[i]):<20} {error_pct:.1f}%")

# =========================================
# SAVE MODEL
# =========================================
print("\n" + "=" * 60)
print("SAVING MODEL")
print("=" * 60)

try:
    # Create backend directory if it doesn't exist
    os.makedirs('backend', exist_ok=True)
    
    model_path = os.path.join('backend', 'model.pkl')
    joblib.dump(model, model_path)
    
    # Save model metadata
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'train_mae': float(train_mae),
        'test_mae': float(test_mae),
        'test_r2': float(test_r2),
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'total_samples': len(X),
        'model_type': 'RandomForestRegressor',
        'categorical_columns': categorical_columns
    }
    
    import json
    metadata_path = os.path.join('backend', 'model_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Model saved to: {model_path}")
    print(f"✓ Metadata saved to: {metadata_path}")
except Exception as e:
    print(f"✗ Error saving model: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✓ TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 60)
print(f"\nModel is ready for deployment!")
print(f"Test R² Score: {test_r2:.4f}")
print(f"Test MAE: ₹ {test_mae:,.2f}")
