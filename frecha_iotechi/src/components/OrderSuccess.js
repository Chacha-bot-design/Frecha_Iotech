// src/components/OrderSuccess.js
import React from 'react';
import './OrderSuccess.css';

const OrderSuccess = ({ orderData, onContinueShopping }) => {
  if (!orderData) {
    return (
      <section className="success-section">
        <div className="container">
          <div className="success-container">
            <div className="text-center">
              <h1 className="success-title">Order Not Found</h1>
              <p className="success-message">There was an issue with your order. Please contact support.</p>
              <button onClick={onContinueShopping} className="continue-btn">
                Continue Shopping
              </button>
            </div>
          </div>
        </div>
      </section>
    );
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-TZ', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatCurrency = (amount) => {
    return `TZS ${amount.toLocaleString()}`;
  };

  return (
    <section className="success-section">
      <div className="container">
        <div className="success-container">
          {/* Success Icon and Title */}
          <div className="success-icon">
            <i className="bi bi-check-lg"></i>
          </div>
          
          <h1 className="success-title">Order Confirmed!</h1>
          <p className="success-subtitle">Thank you for your purchase</p>
          <p className="success-message">
            Your order has been successfully placed and is being processed. 
            We've sent a confirmation email with all the details.
          </p>

          {/* Tracking Information */}
          <div className="tracking-info">
            <div className="tracking-title">Tracking Number</div>
            <div className="tracking-number">TRK-{orderData.id.split('-')[1]}</div>
            <div className="tracking-note">
              Use this number to track your order status
            </div>
          </div>

          {/* Order Details */}
          <div className="order-details">
            <div className="detail-section">
              <h3 className="detail-title">Order Information</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <div className="detail-label">Order ID</div>
                  <div className="detail-value order-id">{orderData.id}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Order Date</div>
                  <div className="detail-value">{formatDate(orderData.orderDate)}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Estimated Delivery</div>
                  <div className="detail-value">{formatDate(orderData.estimatedDelivery)}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Total Amount</div>
                  <div className="detail-value">{formatCurrency(orderData.total)}</div>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3 className="detail-title">Customer Information</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <div className="detail-label">Customer Name</div>
                  <div className="detail-value">{orderData.customer.name}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Email</div>
                  <div className="detail-value">{orderData.customer.email}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Phone</div>
                  <div className="detail-value">{orderData.customer.phone}</div>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3 className="detail-title">Shipping Address</h3>
              <div className="detail-item">
                <div className="detail-value">
                  {orderData.shippingAddress.address}<br />
                  {orderData.shippingAddress.city}, {orderData.shippingAddress.region}<br />
                  {orderData.shippingAddress.postalCode}
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3 className="detail-title">Order Items</h3>
              {orderData.items.map(item => (
                <div key={item.id} className="detail-item">
                  <div className="detail-value">
                    {item.name} × {item.quantity} - {formatCurrency(item.price * item.quantity)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="success-actions">
            <button onClick={onContinueShopping} className="continue-btn">
              <i className="bi bi-cart"></i>
              Continue Shopping
            </button>
            <button onClick={() => window.print()} className="print-btn">
              <i className="bi bi-printer"></i>
              Print Receipt
            </button>
            <button 
              onClick={() => window.location.href = '/track-order'} 
              className="track-btn"
            >
              <i className="bi bi-truck"></i>
              Track Order
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default OrderSuccess;