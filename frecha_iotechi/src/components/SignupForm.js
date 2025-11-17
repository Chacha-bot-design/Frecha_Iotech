// components/SignUpForm.js
import React, { useState } from 'react';
import axios from 'axios';
import { AuthProvider, useAuth } from './AuthContext';

const SignUpForm = ({ cartItems, total, onOrderSuccess, onBack }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone_number: '',
    shipping_address: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { signup } = useAuth();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    // Validate password strength
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      setLoading(false);
      return;
    }

    try {
      // Create account
      const signupResult = await signup({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        phone_number: formData.phone_number
      });

      if (!signupResult.success) {
        setError(signupResult.message);
        setLoading(false);
        return;
      }

      // Create order with user account
      const orderData = {
        customer_name: formData.username,
        customer_email: formData.email,
        customer_phone: formData.phone_number,
        shipping_address: formData.shipping_address,
        items: cartItems.map(item => ({
          product_name: item.name,
          quantity: item.quantity,
          price: item.price
        })),
        total_amount: total,
        notify_via_email: true,
        notify_via_sms: false
      };

      const orderResponse = await axios.post('/api/orders/', orderData);

      if (orderResponse.data.success) {
        onOrderSuccess({
          ...orderResponse.data,
          isNewAccount: true
        });
      } else {
        setError('Order placement failed after account creation');
      }

    } catch (err) {
      console.error('Signup/Order error:', err);
      setError(
        err.response?.data?.message || 
        err.response?.data?.error || 
        'Failed to create account and place order. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
      <div className="mb-6">
        <button 
          onClick={onBack}
          className="flex items-center text-blue-600 hover:text-blue-800 mb-4"
        >
          ← Back to checkout options
        </button>
        <h2 className="text-2xl font-bold text-gray-900">Create Account & Checkout</h2>
        <p className="text-gray-600 mt-2">
          Create an account to track this and future orders easily.
        </p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Account Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Username *
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              minLength="3"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your username"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address *
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="your@email.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password *
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              minLength="6"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="At least 6 characters"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password *
            </label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              required
              minLength="6"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Confirm your password"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleInputChange}
              placeholder="+1234567890"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="md:col-span-2">
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
              placeholder="Enter your complete shipping address"
            />
          </div>
        </div>

        {/* Order Summary */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3">Order Summary</h3>
          {cartItems.map(item => (
            <div key={item.id} className="flex justify-between py-2 border-b border-gray-200">
              <span className="text-gray-700">{item.name} x {item.quantity}</span>
              <span className="font-medium">${(item.price * item.quantity).toFixed(2)}</span>
            </div>
          ))}
          <div className="border-t mt-2 pt-2 font-semibold flex justify-between text-lg">
            <span>Total:</span>
            <span className="text-green-600">${total.toFixed(2)}</span>
          </div>
        </div>

        {/* Benefits Notice */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex">
            <div className="text-green-400 mr-3">✅</div>
            <div>
              <h4 className="font-semibold text-green-800">Account Benefits</h4>
              <ul className="text-green-700 text-sm mt-1 list-disc list-inside space-y-1">
                <li>Track all your orders in one place</li>
                <li>Faster checkout for future orders</li>
                <li>Order history and easy reordering</li>
                <li>Personalized recommendations</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-4 pt-4">
          <button
            type="button"
            onClick={onBack}
            disabled={loading}
            className="flex-1 bg-gray-500 text-white py-3 px-4 rounded-md hover:bg-gray-600 disabled:opacity-50 font-semibold transition duration-200"
          >
            Back to Options
          </button>
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-green-500 text-white py-3 px-4 rounded-md hover:bg-green-600 disabled:opacity-50 font-semibold transition duration-200 flex items-center justify-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating Account...
              </>
            ) : (
              'Create Account & Place Order'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SignUpForm;