// components/UserProfile.js
import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './AuthContext';
import axios from 'axios';

const UserProfile = () => {
  const { user, logout, linkOrderToAccount } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [linkOrderData, setLinkOrderData] = useState({
    order_number: '',
    email: ''
  });
  const [linkMessage, setLinkMessage] = useState('');

  useEffect(() => {
    if (user) {
      fetchUserOrders();
    }
  }, [user]);

  const fetchUserOrders = async () => {
    try {
      const response = await axios.get('/api/orders/my_orders/');
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    }
  };

  const handleLinkOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    setLinkMessage('');

    const result = await linkOrderToAccount(
      linkOrderData.order_number,
      linkOrderData.email
    );

    if (result.success) {
      setLinkMessage('Order linked successfully!');
      setLinkOrderData({ order_number: '', email: '' });
      fetchUserOrders(); // Refresh orders list
    } else {
      setLinkMessage(result.message);
    }
    setLoading(false);
  };

  const handleLogout = async () => {
    await logout();
    window.location.href = '/';
  };

  if (!user) {
    return (
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md text-center">
        <p>Please sign in to view your profile.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">My Account</h2>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Sign Out
        </button>
      </div>

      {/* User Info */}
      <div className="bg-gray-50 p-4 rounded-lg mb-6">
        <h3 className="text-lg font-semibold mb-2">Profile Information</h3>
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Name:</strong> {user.first_name} {user.last_name}</p>
      </div>

      {/* Link Existing Order */}
      <div className="bg-blue-50 p-4 rounded-lg mb-6">
        <h3 className="text-lg font-semibold mb-3">Link Existing Order</h3>
        <p className="text-sm text-gray-600 mb-3">
          Have a guest order? Link it to your account to track it here.
        </p>
        <form onSubmit={handleLinkOrder} className="space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <input
              type="text"
              placeholder="Order Number"
              value={linkOrderData.order_number}
              onChange={(e) => setLinkOrderData(prev => ({
                ...prev,
                order_number: e.target.value
              }))}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <input
              type="email"
              placeholder="Order Email"
              value={linkOrderData.email}
              onChange={(e) => setLinkOrderData(prev => ({
                ...prev,
                email: e.target.value
              }))}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {loading ? 'Linking...' : 'Link Order'}
          </button>
          {linkMessage && (
            <p className={`text-sm ${
              linkMessage.includes('success') ? 'text-green-600' : 'text-red-600'
            }`}>
              {linkMessage}
            </p>
          )}
        </form>
      </div>

      {/* Order History */}
      <div>
        <h3 className="text-lg font-semibold mb-4">Order History</h3>
        {orders.length === 0 ? (
          <p className="text-gray-500">No orders found.</p>
        ) : (
          <div className="space-y-4">
            {orders.map(order => (
              <div key={order.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-semibold">Order #{order.order_number}</h4>
                    <p className="text-sm text-gray-600">
                      Placed on {new Date(order.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <span className={`px-2 py-1 rounded text-sm ${
                    order.status === 'completed' ? 'bg-green-100 text-green-800' :
                    order.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {order.status}
                  </span>
                </div>
                <p className="font-semibold">Total: ${order.total_amount}</p>
                <div className="mt-2">
                  <h5 className="font-medium mb-1">Items:</h5>
                  {order.items.map((item, index) => (
                    <div key={index} className="flex justify-between text-sm">
                      <span>{item.product_name} x {item.quantity}</span>
                      <span>${item.price}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default UserProfile;