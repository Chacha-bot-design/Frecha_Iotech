// src/components/OrderSuccess.js
import React from 'react';

const OrderSuccess = ({ orderData, onContinueShopping }) => {
  return (
    <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md text-center">
      <div className="text-green-500 text-6xl mb-4">✓</div>
      <h2 className="text-3xl font-bold text-gray-800 mb-4">Order Placed Successfully!</h2>
      
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
        <p className="text-lg text-green-800 mb-2">
          Thank you for your order, <strong>{orderData?.customer_name || 'Customer'}</strong>!
        </p>
        <p className="text-green-700">
          Your order number is: <strong>{orderData?.order_number || orderData?.order_id}</strong>
        </p>
        {orderData?.tracking_number && (
          <p className="text-green-700 mt-2">
            Tracking number: <strong>{orderData.tracking_number}</strong>
          </p>
        )}
      </div>

      <div className="text-left bg-gray-50 p-4 rounded-lg mb-6">
        <h3 className="font-semibold mb-3">What happens next?</h3>
        <ul className="list-disc list-inside space-y-2 text-gray-600">
          <li>You will receive a confirmation email at <strong>{orderData?.customer_email}</strong></li>
          <li>We'll send you updates about your order status</li>
          <li>Our team will process your order within 24 hours</li>
          <li>You'll be notified when your order ships</li>
        </ul>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <h4 className="font-semibold text-blue-800 mb-2">Keep your order details safe!</h4>
        <p className="text-blue-700 text-sm">
          Use order number <strong>{orderData?.order_number || orderData?.order_id}</strong> to track your order status.
        </p>
        {orderData?.tracking_number && (
          <p className="text-blue-700 text-sm mt-1">
            Tracking number: <strong>{orderData.tracking_number}</strong>
          </p>
        )}
      </div>

      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          onClick={onContinueShopping}
          className="bg-blue-500 text-white py-3 px-8 rounded-md hover:bg-blue-600 font-semibold"
        >
          Continue Shopping
        </button>
        <button
          onClick={() => window.location.href = '/track-order'}
          className="bg-green-500 text-white py-3 px-8 rounded-md hover:bg-green-600 font-semibold"
        >
          Track Your Order
        </button>
      </div>
    </div>
  );
};

export default OrderSuccess;