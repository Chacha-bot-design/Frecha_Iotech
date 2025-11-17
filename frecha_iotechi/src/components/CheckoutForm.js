// components/CheckoutForm.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AuthProvider, useAuth } from './AuthContext';
import AuthModal from './AuthModal';

const CheckoutForm = ({ cartItems, total, onOrderSuccess, onBackToCart }) => {
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    notify_via_email: true,
    notify_via_sms: false,
    shipping_address: '',
    payment_method: 'credit_card'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showAuthModal, setShowAuthModal] = useState(false);
  const { user, isAuthenticated } = useAuth();

  // Pre-fill form if user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      setFormData(prev => ({
        ...prev,
        customer_name: `${user.first_name} ${user.last_name}`.trim() || user.username,
        customer_email: user.email
      }));
    }
  }, [isAuthenticated, user]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const orderData = {
        ...formData,
        items: cartItems.map(item => ({
          product_name: item.name,
          quantity: item.quantity,
          price: item.price
        })),
        total_amount: total
      };

      const response = await axios.post('/api/orders/', orderData);

      if (response.data.success) {
        onOrderSuccess(response.data);
      } else {
        setError('Failed to place order. Please try again.');
      }
    } catch (err) {
      console.error('Order error:', err);
      setError(err.response?.data?.error || 'Failed to place order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAuthSuccess = () => {
    // Form will be auto-filled due to useEffect
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Checkout</h2>
      
      {/* Auth Status */}
      <div className="mb-6">
        {isAuthenticated ? (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-800 font-medium">
                  Signed in as {user?.username}
                </p>
                <p className="text-green-600 text-sm">
                  Your orders will be saved to your account
                </p>
              </div>
              <button
                onClick={() => setShowAuthModal(true)}
                className="text-green-600 hover:text-green-800 text-sm"
              >
                Switch Account
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-800 font-medium">
                  Continue as guest or create an account
                </p>
                <p className="text-blue-600 text-sm">
                  Create an account to easily track all your orders
                </p>
              </div>
              <button
                onClick={() => setShowAuthModal(true)}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                Sign In / Sign Up
              </button>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Customer Information */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Customer Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                type="text"
                name="customer_name"
                value={formData.customer_name}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                name="customer_email"
                value={formData.customer_email}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phone Number *
              </label>
              <input
                type="tel"
                name="customer_phone"
                value={formData.customer_phone}
                onChange={handleInputChange}
                required
                placeholder="+1234567890"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Shipping Address *
              </label>
              <input
                type="text"
                name="shipping_address"
                value={formData.shipping_address}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Rest of your form remains the same... */}

        <div className="flex space-x-4">
          <button
            type="button"
            onClick={onBackToCart}
            className="flex-1 bg-gray-500 text-white py-3 px-4 rounded-md hover:bg-gray-600"
          >
            Back to Cart
          </button>
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-green-500 text-white py-3 px-4 rounded-md hover:bg-green-600 disabled:opacity-50 font-semibold"
          >
            {loading ? 'Placing Order...' : 'Place Order'}
          </button>
        </div>
      </form>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onSuccess={handleAuthSuccess}
        showGuestOption={true}
      />
    </div>
  );
};

export default CheckoutForm;