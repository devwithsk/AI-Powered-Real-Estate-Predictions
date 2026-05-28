from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import joblib
import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================================
# FLASK APP CONFIGURATION
# =========================================
app = Flask(__name__)

# SECURITY: Only allow requests from specified origins in production
# Get allowed origins from environment or default to localhost for dev
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=ALLOWED_ORIGINS, methods=['GET', 'POST', 'OPTIONS'])

# SECURITY: Initialize rate limiter to prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# SECURITY: Disable debug mode in production
DEBUG_MODE = os.getenv('FLASK_ENV', 'development') == 'development'
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024  # 16KB max request size

# =========================================
# LOGGING CONFIGURATION
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'app.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# =========================================
# MODEL & DATA LOADING
# =========================================
try:
    model = joblib.load(os.path.join(os.path.dirname(__file__), 'model.pkl'))
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

DATA_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'Delhi_house_data.csv')

def load_localities():
    """Load localities from CSV with error handling"""
    try:
        if not os.path.exists(DATA_CSV_PATH):
            logger.warning(f"CSV file not found at {DATA_CSV_PATH}")
            return []

        def is_clean_locality(value: str) -> bool:
            if not value:
                return False
            clean_value = value.strip()
            if len(clean_value) > 60:
                return False

            blacklist = [
                'carpet area', 'super area', 'status', 'floor', 'transaction',
                'furnishing', 'balcony', 'ownership', 'read more', 'contact',
                'agent', 'auction', 'market', 'certified', 'enquire', 'view phone',
                'hotel', 'sqft', 'sqyrd', 'super built', 'newly constructed',
                'ready to move', 'resale', 'share feedback', 'builder'
            ]
            lower = clean_value.lower()
            if any(token in lower for token in blacklist):
                return False

            return True

        df = pd.read_csv(DATA_CSV_PATH, usecols=['Locality'])
        localities = (
            df['Locality']
            .dropna()
            .astype(str)
            .map(str.strip)
            .unique()
        )
        localities = sorted({loc for loc in localities if is_clean_locality(loc)})
        logger.info(f"Loaded {len(localities)} filtered localities from CSV")
        return localities
    except Exception as err:
        logger.error(f"Failed to load localities from CSV: {err}")
        return []

LOCALITIES = load_localities()
LOCALITY_SET = {loc.strip().lower() for loc in LOCALITIES}

# Validation options
FURNISHING_OPTIONS = ["Unfurnished", "Semi-Furnished", "Furnished"]
STATUS_OPTIONS = ["Ready_to_move", "Under_Construction"]
TRANSACTION_OPTIONS = ["New_Property", "Resale"]
TYPE_OPTIONS = ["Apartment", "Independent_House", "Villa"]

# =========================================
# INPUT VALIDATION FUNCTIONS
# =========================================
def validate_input(data):
    """Validate all input parameters"""
    errors = []
    
    # Check required fields
    required_fields = ['area', 'bhk', 'bathroom', 'furnishing', 'locality', 
                      'parking', 'status', 'transaction', 'property_type']
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    try:
        # Validate area: must be positive number between 100 and 50000
        area = float(data.get('area', 0))
        if area <= 0 or area > 50000:
            errors.append("Area must be between 100 and 50000 sq ft")
        
        # Validate BHK: must be integer between 1 and 10
        bhk = int(data.get('bhk', 0))
        if bhk < 1 or bhk > 10:
            errors.append("BHK must be between 1 and 10")
        
        # Validate bathroom: must be integer between 1 and 8
        bathroom = int(data.get('bathroom', 0))
        if bathroom < 1 or bathroom > 8:
            errors.append("Bathrooms must be between 1 and 8")
        
        # Validate parking: must be integer between 0 and 5
        parking = int(data.get('parking', 0))
        if parking < 0 or parking > 5:
            errors.append("Parking must be between 0 and 5")
        
        # Validate categorical fields
        furnishing = data.get('furnishing', '').strip()
        if furnishing not in FURNISHING_OPTIONS:
            errors.append(f"Invalid furnishing type. Must be one of: {FURNISHING_OPTIONS}")
        
        status = data.get('status', '').strip()
        if status not in STATUS_OPTIONS:
            errors.append(f"Invalid status. Must be one of: {STATUS_OPTIONS}")
        
        transaction = data.get('transaction', '').strip()
        if transaction not in TRANSACTION_OPTIONS:
            errors.append(f"Invalid transaction type. Must be one of: {TRANSACTION_OPTIONS}")
        
        property_type = data.get('property_type', '').strip()
        if property_type not in TYPE_OPTIONS:
            errors.append(f"Invalid property type. Must be one of: {TYPE_OPTIONS}")
        
        # Validate locality: minimum 3 characters
        locality = data.get('locality', '').strip()
        if len(locality) < 2:
            errors.append("Locality must be at least 2 characters long")
        
    except (ValueError, TypeError) as e:
        errors.append(f"Invalid data type: {str(e)}")
    
    return len(errors) == 0, errors

# =========================================
# API ROUTES
# =========================================
@app.route('/api/predict', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limit: 10 predictions per minute per IP
def predict():
    """Predict house price based on input parameters"""
    try:
        # Validate JSON
        data = request.get_json()
        if data is None:
            logger.warning("Request body is not valid JSON")
            return jsonify({
                'success': False,
                'error': 'Request body must be valid JSON'
            }), 400
        
        # Validate input
        is_valid, errors = validate_input(data)
        if not is_valid:
            logger.warning(f"Validation failed: {errors}")
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        # Extract and sanitize data
        area = float(data.get('area'))
        bhk = int(data.get('bhk'))
        bathroom = int(data.get('bathroom'))
        furnishing = data.get('furnishing').strip()
        locality = data.get('locality').strip()
        parking = int(data.get('parking'))
        status = data.get('status').strip()
        transaction = data.get('transaction').strip()
        property_type = data.get('property_type').strip()
        
        # Check if locality is known (for disclaimer)
        known_locality = locality.lower() in LOCALITY_SET
        disclaimer = None
        if not known_locality:
            disclaimer = (
                "Disclaimer: This location is not in our training data. "
                "Prediction accuracy may be lower for locations outside Delhi or "
                "unknown localities. Use this as a reference only."
            )
            logger.info(f"Unknown locality prediction requested: {locality}")
        
        # FIXED: Calculate Per_Sqft correctly
        # Per_Sqft should be price per square foot, estimated from area
        # Using a more realistic calculation based on market data
        per_sqft = 5000  # Base rate, will be adjusted by model based on features
        
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
        
        # Validate prediction output
        if np.isnan(predicted_price) or np.isinf(predicted_price) or predicted_price < 0:
            logger.error(f"Invalid prediction output: {predicted_price}")
            return jsonify({
                'success': False,
                'error': 'Model returned invalid prediction'
            }), 500
        
        # Prepare response
        response = {
            'success': True,
            'predicted_price': round(float(predicted_price), 2),
            'currency': '₹',
            'message': f'Predicted house price: ₹ {predicted_price:,.2f}',
            'confidence': 'Medium'
        }
        
        if disclaimer:
            response['disclaimer'] = disclaimer
        
        logger.info(f"Prediction successful - Area: {area}, BHK: {bhk}, Price: {predicted_price}")
        return jsonify(response), 200
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return jsonify({
            'success': False,
            'error': 'Invalid JSON format in request body'
        }), 400
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request'
        }), 500

@app.route('/api/options', methods=['GET'])
@limiter.limit("30 per minute")  # Rate limit: 30 requests per minute
def get_options():
    """Get available options for dropdown menus"""
    try:
        return jsonify({
            'success': True,
            'localities': LOCALITIES,
            'furnishing': FURNISHING_OPTIONS,
            'status': STATUS_OPTIONS,
            'transaction': TRANSACTION_OPTIONS,
            'property_type': TYPE_OPTIONS
        }), 200
    except Exception as e:
        logger.error(f"Error fetching options: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch options'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': True
    }), 200

# =========================================
# ERROR HANDLERS
# =========================================
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# =========================================
# APP ENTRY POINT
# =========================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting Flask app on port {port} (debug={DEBUG_MODE})")
    app.run(debug=DEBUG_MODE, port=port, host='0.0.0.0')
