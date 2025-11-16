// components/GuestCheckout.js
import React, { useState } from 'react';
import axios from 'axios';

const GuestCheckout = ({ cartItems, total, onOrderSuccess, onBack }) => {
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    notify_via_email: true,
    notify_via_sms: false,
    shipping_address: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
      setError(err.response?.data?.message || 'Failed to place order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Guest Checkout</h2>
        <p className="text-gray-600 mt-2">
          Complete your order quickly. You'll receive tracking information via email.
        </p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Customer Information */}
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
              Phone Number
            </label>
            <input
              type="tel"
              name="customer_phone"
              value={formData.customer_phone}
              onChange={handleInputChange}
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

        {/* Notification Preferences */}
        <div className="border-t pt-6">
          <h3 className="text-lg font-semibold mb-4">Notification Preferences</h3>
          <div className="space-y-3">
            <label className="flex items-center">
              <input
                type="checkbox"
                name="notify_via_email"
                checked={formData.notify_via_email}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 rounded"
              />
              <span className="ml-2 text-gray-700">Send order updates via email</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="notify_via_sms"
                checked={formData.notify_via_sms}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 rounded"
              />
              <span className="ml-2 text-gray-700">Send order updates via SMS</span>
            </label>
          </div>
        </div>

        {/* Order Summary */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3">Order Summary</h3>
          {cartItems.map(item => (
            <div key={item.id} className="flex justify-between py-2">
              <span>{item.name} x {item.quantity}</span>
              <span>${(item.price * item.quantity).toFixed(2)}</span>
            </div>
          ))}
          <div className="border-t mt-2 pt-2 font-semibold flex justify-between">
            <span>Total:</span>
            <span>${total.toFixed(2)}</span>
          </div>
        </div>

        {/* Guest Notice */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex">
            <div className="text-yellow-400 mr-3">💡</div>
            <div>
              <h4 className="font-semibold text-yellow-800">Guest Order Notice</h4>
              <p className="text-yellow-700 text-sm mt-1">
                You're checking out as a guest. You can track your order using your email and order number. 
                Consider creating an account to easily track all your orders in one place.
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-4">
          <button
            type="button"
            onClick={onBack}
            className="flex-1 bg-gray-500 text-white py-3 px-4 rounded-md hover:bg-gray-600"
          >
            Back to Options
          </button>
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-green-500 text-white py-3 px-4 rounded-md hover:bg-green-600 disabled:opacity-50 font-semibold"
          >
            {loading ? 'Placing Order...' : 'Place Guest Order'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default GuestCheckout;