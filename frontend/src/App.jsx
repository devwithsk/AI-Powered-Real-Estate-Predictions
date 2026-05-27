import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Format Indian Price (Crore, Lakh format)
const formatIndianPrice = (price) => {
  const isNegative = price < 0;
  const absPrice = Math.abs(price);
  let formatted = '';

  if (absPrice >= 10000000) {
    formatted = `₹ ${(absPrice / 10000000).toFixed(2)} Cr`;
  } else if (absPrice >= 100000) {
    formatted = `₹ ${(absPrice / 100000).toFixed(2)} Lakh`;
  } else {
    formatted = `₹ ${absPrice.toLocaleString("en-IN")}`;
  }

  return isNegative ? `- ${formatted}` : formatted;
};

function App() {
  const [formData, setFormData] = useState({
    area: '',
    bhk: '',
    bathroom: '',
    furnishing: 'Semi-Furnished',
    locality: '',
    parking: '',
    status: 'Ready_to_move',
    transaction: 'New_Property',
    property_type: 'Apartment',
  });

  const [options, setOptions] = useState({
    localities: [],
    furnishing: [],
    status: [],
    transaction: [],
    property_type: [],
  });

  const [prediction, setPrediction] = useState(null);
  const [disclaimer, setDisclaimer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [localitySearch, setLocalitySearch] = useState('');
  const [showLocalityDropdown, setShowLocalityDropdown] = useState(false);

  useEffect(() => {
    fetchOptions();
  }, []);

  const fetchOptions = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/options');
      setOptions({
        localities: response.data.localities,
        furnishing: response.data.furnishing,
        status: response.data.status,
        transaction: response.data.transaction,
        property_type: response.data.property_type,
      });
    } catch (err) {
      console.error('Error fetching options:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLocalitySearch = (e) => {
    const value = e.target.value;
    setLocalitySearch(value);
    setFormData(prev => ({
      ...prev,
      locality: value
    }));
    setShowLocalityDropdown(value.length > 0);
  };

  const handleLocalitySelect = (loc) => {
    setFormData(prev => ({
      ...prev,
      locality: loc
    }));
    setLocalitySearch(loc);
    setShowLocalityDropdown(false);
  };

  const filteredLocalities = options.localities.filter(loc =>
    loc.toLowerCase().includes(localitySearch.toLowerCase())
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);

    try {
      const response = await axios.post('http://localhost:5000/api/predict', formData);
      setPrediction(response.data.predicted_price);
      setDisclaimer(response.data.disclaimer || '');
    } catch (err) {
      setError(err.response?.data?.error || 'Error making prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleNewPrediction = () => {
    setPrediction(null);
    setError('');
    setFormData({
      area: '',
      bhk: '',
      bathroom: '',
      furnishing: 'Semi-Furnished',
      locality: '',
      parking: '',
      status: 'Ready_to_move',
      transaction: 'New_Property',
      property_type: 'Apartment',
    });
    setLocalitySearch('');
  };

  // Results Page View
  if (prediction) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-blue-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Success Header */}
          <div className="text-center mb-16">
            <div className="inline-block bg-green-100 rounded-full p-4 mb-6">
              <span className="text-5xl">✓</span>
            </div>
            <h1 className="text-5xl font-black text-gray-900 mb-3">
              Your Property Valuation
            </h1>
            <p className="text-xl text-gray-600">
              AI-Powered Market Analysis for Your Delhi Property
            </p>
          </div>

          {/* Main Price Display - Hero Section */}
          <div className="bg-gradient-to-br from-blue-600 to-indigo-600 rounded-3xl shadow-2xl overflow-hidden mb-12 transform hover:scale-105 transition-transform duration-300">
            <div className="px-8 py-16 sm:px-16 text-center">
              <p className="text-blue-100 text-lg mb-4 uppercase tracking-wider font-semibold">
                Estimated Property Value
              </p>
              <p className="text-7xl font-black text-white mb-6">
                {formatIndianPrice(prediction)}
              </p>
              <p className="text-blue-100 text-base">
                Based on current Delhi housing market analysis
              </p>
            </div>
          </div>

          {disclaimer && (
            <div className="mb-8 rounded-3xl border border-yellow-300 bg-yellow-50 p-6 text-yellow-900 shadow-sm">
              <p className="font-semibold mb-2">Disclaimer</p>
              <p>{disclaimer}</p>
            </div>
          )}

          {/* Market Range Card */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-2xl shadow-lg p-8 border-l-4 border-orange-400">
              <p className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-3">
                Conservative Estimate
              </p>
              <p className="text-3xl font-bold text-orange-600">
                {formatIndianPrice(prediction * 0.9)}
              </p>
              <p className="text-gray-500 text-xs mt-2">-10% from base prediction</p>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl shadow-lg p-8 border-l-4 border-green-500 border-t-4">
              <p className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-3">
                Market Price
              </p>
              <p className="text-3xl font-bold text-green-600">
                {formatIndianPrice(prediction)}
              </p>
              <p className="text-gray-500 text-xs mt-2">AI-Predicted Value</p>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-8 border-l-4 border-blue-400">
              <p className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-3">
                Optimistic Estimate
              </p>
              <p className="text-3xl font-bold text-blue-600">
                {formatIndianPrice(prediction * 1.1)}
              </p>
              <p className="text-gray-500 text-xs mt-2">+10% from base prediction</p>
            </div>
          </div>

          {/* Property Summary - Detailed Card */}
          <div className="bg-white rounded-2xl shadow-xl p-10 mb-12 border-t-4 border-indigo-600">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center gap-3">
              <span className="text-indigo-600">📋</span>
              Your Property Details
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="flex items-center gap-4 p-4 bg-blue-50 rounded-xl">
                <div className="text-3xl">📐</div>
                <div>
                  <p className="text-gray-600 text-sm font-medium">Area</p>
                  <p className="text-2xl font-bold text-gray-900">{formData.area} sq ft</p>
                </div>
              </div>

              <div className="flex items-center gap-4 p-4 bg-purple-50 rounded-xl">
                <div className="text-3xl">🏠</div>
                <div>
                  <p className="text-gray-600 text-sm font-medium">BHK Configuration</p>
                  <p className="text-2xl font-bold text-gray-900">{formData.bhk} BHK</p>
                </div>
              </div>

              <div className="flex items-center gap-4 p-4 bg-pink-50 rounded-xl">
                <div className="text-3xl">🚿</div>
                <div>
                  <p className="text-gray-600 text-sm font-medium">Bathrooms</p>
                  <p className="text-2xl font-bold text-gray-900">{formData.bathroom}</p>
                </div>
              </div>

              <div className="flex items-center gap-4 p-4 bg-yellow-50 rounded-xl">
                <div className="text-3xl">🚗</div>
                <div>
                  <p className="text-gray-600 text-sm font-medium">Parking Slots</p>
                  <p className="text-2xl font-bold text-gray-900">{formData.parking}</p>
                </div>
              </div>

              <div className="md:col-span-2 flex items-center gap-4 p-4 bg-green-50 rounded-xl">
                <div className="text-3xl">📍</div>
                <div>
                  <p className="text-gray-600 text-sm font-medium">Location</p>
                  <p className="text-2xl font-bold text-gray-900">{formData.locality}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Additional Property Info */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-xl p-6 border border-orange-200">
              <p className="text-orange-600 font-bold text-sm mb-1">FURNISHING</p>
              <p className="text-gray-900 font-semibold text-lg">{formData.furnishing}</p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
              <p className="text-blue-600 font-bold text-sm mb-1">PROPERTY TYPE</p>
              <p className="text-gray-900 font-semibold text-lg">{formData.property_type}</p>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
              <p className="text-green-600 font-bold text-sm mb-1">STATUS</p>
              <p className="text-gray-900 font-semibold text-lg">{formData.status}</p>
            </div>
          </div>

          {/* CTA Section */}
          <div className="bg-gradient-to-r from-indigo-600 to-blue-600 rounded-2xl p-10 text-center mb-12 shadow-lg">
            <h3 className="text-2xl font-bold text-white mb-3">Ready to Explore More Options?</h3>
            <p className="text-indigo-100 mb-6">Analyze another property or refine your current search</p>
            <button
              onClick={handleNewPrediction}
              className="bg-white text-indigo-600 font-bold py-3 px-8 rounded-lg hover:bg-indigo-50 transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              ✨ Analyze Another Property
            </button>
          </div>

          {/* Trust Indicators */}
          <div className="text-center">
            <p className="text-gray-600 mb-4">🧠 Powered by Machine Learning trained on Delhi housing market data</p>
            <div className="flex justify-center gap-8 text-sm text-gray-500">
              <span>✓ Real-time Analysis</span>
              <span>✓ 0.85 R² Accuracy</span>
              <span>✓ 1000+ Properties Analyzed</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Input Form View
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🏠 House Price Predictor</h1>
          <p className="text-lg text-gray-600">AI-Powered Price Prediction for Delhi Properties</p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-8 sm:px-10">
            <h2 className="text-2xl font-bold text-white">Enter Property Details</h2>
            <p className="text-blue-100 text-sm mt-1">Get instant AI-powered valuation in seconds</p>
          </div>

          <form onSubmit={handleSubmit} className="px-6 py-8 sm:px-10">
            {/* Area and BHK Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Area (sq ft)
                </label>
                <input
                  type="number"
                  name="area"
                  value={formData.area}
                  onChange={handleChange}
                  placeholder="e.g., 1200"
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  BHK
                </label>
                <select
                  name="bhk"
                  value={formData.bhk}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  <option value="">Select BHK</option>
                  {[1, 2, 3, 4, 5, 6].map(num => (
                    <option key={num} value={num}>{num} BHK</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Bathroom and Parking Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bathrooms
                </label>
                <select
                  name="bathroom"
                  value={formData.bathroom}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  <option value="">Select Bathrooms</option>
                  {[1, 2, 3, 4, 5].map(num => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Parking
                </label>
                <select
                  name="parking"
                  value={formData.parking}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  <option value="">Select Parking</option>
                  {[0, 1, 2, 3, 4].map(num => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Locality Row */}
            <div className="mb-6 relative">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Locality
              </label>
              <input
                type="text"
                value={localitySearch}
                onChange={handleLocalitySearch}
                onFocus={() => setShowLocalityDropdown(true)}
                placeholder="Type locality..."
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              />
              {showLocalityDropdown && filteredLocalities.length > 0 && (
                <div className="absolute z-10 w-full mt-2 bg-white border border-gray-300 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                  {filteredLocalities.map(loc => (
                    <div
                      key={loc}
                      onClick={() => handleLocalitySelect(loc)}
                      className="px-4 py-2 hover:bg-blue-100 cursor-pointer transition"
                    >
                      {loc}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Furnishing and Type Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Furnishing
                </label>
                <select
                  name="furnishing"
                  value={formData.furnishing}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  {options.furnishing.map(f => (
                    <option key={f} value={f}>{f}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Property Type
                </label>
                <select
                  name="property_type"
                  value={formData.property_type}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  {options.property_type.map(t => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Status and Transaction Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  {options.status.map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Transaction Type
                </label>
                <select
                  name="transaction"
                  value={formData.transaction}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  {options.transaction.map(t => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 font-semibold">❌ {error}</p>
              </div>
            )}

            {/* Submit Button with Loading Animation */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-3 px-4 rounded-lg hover:shadow-lg transform hover:scale-105 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <span className="animate-spin">⏳</span>
                  <span>Analyzing Property...</span>
                </>
              ) : (
                '🔮 Predict Price'
              )}
            </button>
          </form>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600">
          <p className="font-semibold">🧠 Powered by Machine Learning trained on Delhi housing market data</p>
        </div>
      </div>
    </div>
  );
}

export default App;
