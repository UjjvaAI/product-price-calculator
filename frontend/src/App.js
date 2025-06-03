import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Main Calculator Component
const ProductCalculator = () => {
  const [formData, setFormData] = useState({
    product_name: '',
    quantity: '',
    unit_price_before_tax: '',
    gst_percentage: '18',
    sales_price_mrp_per_unit: ''
  });

  const [calculationResult, setCalculationResult] = useState(null);
  const [gstRates, setGstRates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);

  // Fetch GST rates on component mount
  useEffect(() => {
    fetchGstRates();
    fetchCalculationHistory();
  }, []);

  const fetchGstRates = async () => {
    try {
      const response = await axios.get(`${API}/gst-rates`);
      setGstRates(response.data.common_rates);
    } catch (error) {
      console.error('Error fetching GST rates:', error);
    }
  };

  const fetchCalculationHistory = async () => {
    try {
      const response = await axios.get(`${API}/calculations?limit=10`);
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const validateForm = () => {
    const { product_name, quantity, unit_price_before_tax, gst_percentage, sales_price_mrp_per_unit } = formData;
    
    if (!product_name.trim()) return 'Product name is required';
    if (!quantity || parseFloat(quantity) <= 0) return 'Quantity must be greater than 0';
    if (!unit_price_before_tax || parseFloat(unit_price_before_tax) < 0) return 'Unit price must be 0 or greater';
    if (!gst_percentage || parseFloat(gst_percentage) < 0 || parseFloat(gst_percentage) > 100) return 'GST percentage must be between 0-100';
    if (!sales_price_mrp_per_unit || parseFloat(sales_price_mrp_per_unit) <= 0) return 'Sales price must be greater than 0';
    
    return null;
  };

  const handleCalculate = async (e) => {
    e.preventDefault();
    
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const requestData = {
        product_name: formData.product_name.trim(),
        quantity: parseFloat(formData.quantity),
        unit_price_before_tax: parseFloat(formData.unit_price_before_tax),
        gst_percentage: parseFloat(formData.gst_percentage),
        sales_price_mrp_per_unit: parseFloat(formData.sales_price_mrp_per_unit)
      };

      const response = await axios.post(`${API}/calculate`, requestData);
      setCalculationResult(response.data);
      
      // Save to history
      await saveCalculationToHistory(response.data);
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Error performing calculation');
      console.error('Calculation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveCalculationToHistory = async (result) => {
    try {
      await axios.post(`${API}/calculations`, result);
      fetchCalculationHistory(); // Refresh history
    } catch (error) {
      console.error('Error saving to history:', error);
    }
  };

  const clearForm = () => {
    setFormData({
      product_name: '',
      quantity: '',
      unit_price_before_tax: '',
      gst_percentage: '18',
      sales_price_mrp_per_unit: ''
    });
    setCalculationResult(null);
    setError('');
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(amount);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Product Pricing Calculator</h1>
          <p className="text-gray-600">Calculate taxes, margins, and markup percentages for your products</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Input Form */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Product Details</h2>
            
            <form onSubmit={handleCalculate} className="space-y-4">
              {/* Product Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Product Name *
                </label>
                <input
                  type="text"
                  name="product_name"
                  value={formData.product_name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter product name"
                  required
                />
              </div>

              {/* Quantity */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quantity *
                </label>
                <input
                  type="number"
                  name="quantity"
                  value={formData.quantity}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter quantity"
                  min="0.01"
                  step="0.01"
                  required
                />
              </div>

              {/* Unit Price Before Tax */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Unit Price (Before Tax) *
                </label>
                <input
                  type="number"
                  name="unit_price_before_tax"
                  value={formData.unit_price_before_tax}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter unit price before tax"
                  min="0"
                  step="0.01"
                  required
                />
              </div>

              {/* GST Percentage */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  GST Percentage *
                </label>
                <select
                  name="gst_percentage"
                  value={formData.gst_percentage}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                >
                  {gstRates.map((rate) => (
                    <option key={rate.rate} value={rate.rate}>
                      {rate.description}
                    </option>
                  ))}
                </select>
                <div className="mt-2">
                  <input
                    type="number"
                    name="gst_percentage"
                    value={formData.gst_percentage}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Or enter custom GST percentage"
                    min="0"
                    max="100"
                    step="0.01"
                  />
                </div>
              </div>

              {/* Sales Price MRP */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sales Price/MRP (Per Unit) *
                </label>
                <input
                  type="number"
                  name="sales_price_mrp_per_unit"
                  value={formData.sales_price_mrp_per_unit}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter sales price per unit"
                  min="0.01"
                  step="0.01"
                  required
                />
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-md p-3">
                  <p className="text-red-600 text-sm">{error}</p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex space-x-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Calculating...' : 'Calculate'}
                </button>
                <button
                  type="button"
                  onClick={clearForm}
                  className="flex-1 bg-gray-500 text-white py-2 px-4 rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500"
                >
                  Clear
                </button>
              </div>
            </form>
          </div>

          {/* Right Column - Calculation Results */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Calculation Results</h2>
            
            {calculationResult ? (
              <div className="space-y-4">
                {/* Product Info */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-blue-800 text-lg">{calculationResult.product_name}</h3>
                  <p className="text-blue-600">Calculation ID: {calculationResult.calculation_id.slice(0, 8)}</p>
                </div>

                {/* Calculation Details */}
                <div className="grid grid-cols-1 gap-3">
                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Product Quantity:</span>
                    <span className="font-medium">{calculationResult.quantity}</span>
                  </div>

                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Unit Price (Before Tax):</span>
                    <span className="font-medium">{formatCurrency(calculationResult.unit_price_before_tax)}</span>
                  </div>

                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Subtotal (Before Tax):</span>
                    <span className="font-medium">{formatCurrency(calculationResult.subtotal_before_tax)}</span>
                  </div>

                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Tax ({calculationResult.tax_name}):</span>
                    <span className="font-medium text-orange-600">{calculationResult.gst_percentage}%</span>
                  </div>

                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Unit Price (After Tax):</span>
                    <span className="font-medium">{formatCurrency(calculationResult.unit_price_after_tax)}</span>
                  </div>

                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Subtotal (After Tax):</span>
                    <span className="font-medium">{formatCurrency(calculationResult.subtotal_after_tax)}</span>
                  </div>

                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Effective Rate (Per Unit):</span>
                    <span className="font-medium">{formatCurrency(calculationResult.effective_rate_per_unit)}</span>
                  </div>

                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Sales Price/MRP (Per Unit):</span>
                    <span className="font-medium text-green-600">{formatCurrency(calculationResult.sales_price_mrp_per_unit)}</span>
                  </div>
                </div>

                {/* Profit Analysis */}
                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-3">Profit Analysis</h4>
                  <div className="grid grid-cols-1 gap-2">
                    <div className="flex justify-between items-center">
                      <span className="text-green-700">Margin Percentage:</span>
                      <span className="font-bold text-green-800 text-lg">{calculationResult.margin_percentage}%</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-green-700">Markup Percentage:</span>
                      <span className="font-bold text-green-800 text-lg">{calculationResult.markup_percentage}%</span>
                    </div>
                  </div>
                </div>

                {/* Timestamp */}
                <div className="text-sm text-gray-500 text-center">
                  Calculated at: {new Date(calculationResult.timestamp).toLocaleString()}
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-500 py-12">
                <div className="text-6xl mb-4">📊</div>
                <p>Enter product details and click "Calculate" to see results</p>
              </div>
            )}
          </div>
        </div>

        {/* Calculation History */}
        {history.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Recent Calculations</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {history.slice(0, 6).map((entry) => (
                <div key={entry.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <h4 className="font-medium text-gray-800 truncate">{entry.calculation_result.product_name}</h4>
                  <p className="text-sm text-gray-600">Qty: {entry.calculation_result.quantity}</p>
                  <p className="text-sm text-gray-600">GST: {entry.calculation_result.gst_percentage}%</p>
                  <p className="text-sm text-green-600 font-medium">Margin: {entry.calculation_result.margin_percentage}%</p>
                  <p className="text-xs text-gray-400">{new Date(entry.saved_at).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <ProductCalculator />
    </div>
  );
}

export default App;
