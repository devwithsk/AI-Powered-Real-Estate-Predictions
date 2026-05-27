import pandas as pd
import numpy as np
import joblib

# Machine Learning Libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Encoding
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# =========================================
# STEP 1 — LOAD DATASET
# =========================================

df = pd.read_csv("Delhi_house_data.csv")

print("Dataset Loaded Successfully!\n")

print(df.head())

# =========================================
# STEP 2 — HANDLE MISSING VALUES
# =========================================

# Numerical columns
numerical_columns = [
    "Area",
    "BHK",
    "Bathroom",
    "Parking"
]

# Fill numerical missing values with mean
num_imputer = SimpleImputer(strategy="mean")

df[numerical_columns] = num_imputer.fit_transform(
    df[numerical_columns]
)

# Categorical columns
categorical_fill_columns = [
    "Furnishing",
    "Locality",
    "Status",
    "Transaction",
    "Type"
]

# Fill categorical missing values with most frequent value
cat_imputer = SimpleImputer(strategy="most_frequent")

df[categorical_fill_columns] = cat_imputer.fit_transform(
    df[categorical_fill_columns]
)

# =========================================
# FEATURE ENGINEERING
# =========================================

# Total rooms feature
df["TotalRooms"] = df["BHK"] + df["Bathroom"]

# =========================================
# HANDLE Per_Sqft MISSING VALUES
# =========================================

df["Per_Sqft"] = df["Per_Sqft"].fillna(
    df["Per_Sqft"].median()
)

# =========================================
# REMOVE OUTLIERS USING IQR
# =========================================

Q1 = df["Price"].quantile(0.25)

Q3 = df["Price"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR

upper_limit = Q3 + 1.5 * IQR

df = df[
    (df["Price"] >= lower_limit) &
    (df["Price"] <= upper_limit)
]

print("\nOutliers Removed Successfully!")

print(f"Remaining Rows: {len(df)}")

# =========================================
# STEP 3 — FEATURES & TARGET
# =========================================

X = df.drop("Price", axis=1)

y = df["Price"]

# =========================================
# STEP 4 — CATEGORICAL COLUMNS
# =========================================

categorical_columns = [
    "Furnishing",
    "Locality",
    "Status",
    "Transaction",
    "Type"
]

# =========================================
# STEP 5 — PREPROCESSING
# =========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        )
    ],
    remainder="passthrough"
)

# =========================================
# STEP 6 — CREATE PIPELINE
# =========================================

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        max_depth=20,
        min_samples_split=5
    ))
])

# =========================================
# STEP 7 — TRAIN TEST SPLIT
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================================
# STEP 8 — TRAIN MODEL
# =========================================

model.fit(X_train, y_train)

print("\nModel Training Completed!")

# =========================================
# STEP 9 — PREDICTIONS
# =========================================

predictions = model.predict(X_test)

print("\nSome Predictions:\n")

for i in range(5):
    print(f"Predicted: ₹ {predictions[i]:.2f}")
    print(f"Actual:    ₹ {y_test.iloc[i]:.2f}")
    print()

# =========================================
# STEP 10 — MODEL EVALUATION
# =========================================

mae = mean_absolute_error(y_test, predictions)

r2 = r2_score(y_test, predictions)

print("Model Performance:\n")

print(f"Mean Absolute Error: ₹ {mae:.2f}")

print(f"R2 Score: {r2:.2f}")

# =========================================
# STEP 11 — CUSTOM PREDICTION
# =========================================

sample_house = pd.DataFrame({
    "Area": [1200],
    "BHK": [3],
    "Bathroom": [2],
    "Furnishing": ["Semi-Furnished"],
    "Locality": ["Rohini Sector 24"],
    "Parking": [1],
    "Status": ["Ready_to_move"],
    "Transaction": ["New_Property"],
    "Type": ["Apartment"],
    "Per_Sqft": [6500]
})

# Feature Engineering for sample input
sample_house["TotalRooms"] = (
    sample_house["BHK"] +
    sample_house["Bathroom"]
)

predicted_price = model.predict(sample_house)

print("\nPredicted House Price:\n")

print(f"₹ {predicted_price[0]:.2f}")

# =========================================
# STEP 12 — SAVE MODEL
# =========================================

joblib.dump(model, "model.pkl")

print("\nModel Saved Successfully!")