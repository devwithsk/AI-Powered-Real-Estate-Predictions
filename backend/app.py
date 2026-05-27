from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

model = joblib.load(os.path.join(os.path.dirname(__file__), 'model.pkl'))

DATA_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'Delhi_house_data.csv')


def load_localities():
    try:
        df = pd.read_csv(DATA_CSV_PATH, usecols=['Locality'])
        localities = (
            df['Locality']
            .dropna()
            .astype(str)
            .map(str.strip)
            .unique()
        )
        localities = sorted([loc for loc in localities if loc])
        return localities
    except Exception as err:
        print(f"Failed to load localities from CSV: {err}")
        return []

LOCALITIES = load_localities()
LOCALITY_SET = {loc.strip().lower() for loc in LOCALITIES}

FURNISHING_OPTIONS = ["Unfurnished", "Semi-Furnished", "Furnished"]
STATUS_OPTIONS = ["Ready_to_move", "Under_Construction"]
TRANSACTION_OPTIONS = ["New_Property", "Resale"]
TYPE_OPTIONS = ["Apartment", "Independent_House", "Villa"]

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        area = float(data.get('area'))
        bhk = int(data.get('bhk'))
        bathroom = int(data.get('bathroom'))
        furnishing = data.get('furnishing')
        locality = data.get('locality')
        parking = int(data.get('parking'))
        status = data.get('status')
        transaction = data.get('transaction')
        property_type = data.get('property_type')

        # Determine whether locality is outside the trained CSV list
        known_locality = locality and locality.strip().lower() in LOCALITY_SET
        disclaimer = None
        if not known_locality:
            disclaimer = (
                "Disclaimer: AI is trained only on Delhi housing market data. "
                "Results for locations outside Delhi may be less accurate."
            )

        # Calculate Per_Sqft
        per_sqft = (area / 100) * 5000

        # Create DataFrame for prediction
        input_data = pd.DataFrame({
            "Area": [area],
            "BHK": [bhk],
            "Bathroom": [bathroom],
            "Furnishing": [furnishing],
            "Locality": [locality],
            "Parking": [parking],
            "Status": [status],
            "Transaction": [transaction],
            "Type": [property_type],
            "Per_Sqft": [per_sqft]
        })

        # Feature Engineering
        input_data["TotalRooms"] = input_data["BHK"] + input_data["Bathroom"]

        # Make prediction
        predicted_price = model.predict(input_data)[0]

        response = {
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'currency': '₹',
            'message': f'Predicted house price: ₹ {predicted_price:,.2f}'
        }

        if disclaimer:
            response['disclaimer'] = disclaimer

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/options', methods=['GET'])
def get_options():
    return jsonify({
        'localities': LOCALITIES,
        'furnishing': FURNISHING_OPTIONS,
        'status': STATUS_OPTIONS,
        'transaction': TRANSACTION_OPTIONS,
        'property_type': TYPE_OPTIONS
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
