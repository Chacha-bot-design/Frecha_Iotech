import React, { useState } from 'react';
import { trackOrder } from '../services/api';
import './OrderTracking.css';

const OrderTracking = () => {
  const [trackingNumber, setTrackingNumber] = useState('');
  const [orderDetails, setOrderDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [recentSearches, setRecentSearches] = useState([]);

  // Load recent searches from localStorage on component mount
  React.useEffect(() => {
    const saved = localStorage.getItem('recentOrderSearches');
    if (saved) {
      setRecentSearches(JSON.parse(saved));
    }
  }, []);

  // Save to recent searches
  const saveToRecentSearches = (trackingNum) => {
    const updated = [trackingNum, ...recentSearches.filter(item => item !== trackingNum)].slice(0, 5);
    setRecentSearches(updated);
    localStorage.setItem('recentOrderSearches', JSON.stringify(updated));
  };

  const handleTrackOrder = async (e) => {
    e.preventDefault();
    if (!trackingNumber.trim()) {
      setError('Please enter a tracking number');
      return;
    }

    setLoading(true);
    setError('');
    setOrderDetails(null);

    try {
      const response = await trackOrder(trackingNumber.toUpperCase());
      setOrderDetails(response);
      saveToRecentSearches(trackingNumber.toUpperCase());
    } catch (err) {
      setError(err.response?.data?.error || 'Order not found. Please check your tracking number.');
      setOrderDetails(null);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const statusColors = {
      'pending': '#f39c12',      // Orange
      'confirmed': '#3498db',    // Blue
      'processing': '#9b59b6',   // Purple
      'shipped': '#e67e22',      // Dark Orange
      'delivered': '#27ae60',    // Green
      'cancelled': '#e74c3c'     // Red
    };
    return statusColors[status] || '#95a5a6';
  };

  const getStatusIcon = (status) => {
    const statusIcons = {
      'pending': '⏳',
      'confirmed': '✅',
      'processing': '🔧',
      'shipped': '🚚',
      'delivered': '📦',
      'cancelled': '❌'
    };
    return statusIcons[status] || '📋';
  };

  const getStatusDescription = (status) => {
    const descriptions = {
      'pending': 'Your order has been received and is waiting for confirmation.',
      'confirmed': 'Your order has been confirmed and is being prepared.',
      'processing': 'We are currently processing your order.',
      'shipped': 'Your order has been shipped and is on its way.',
      'delivered': 'Your order has been successfully delivered.',
      'cancelled': 'This order has been cancelled.'
    };
    return descriptions[status] || 'Status update available.';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="order-tracking-container">
      <div className="tracking-header">
        <h1>Track Your Order</h1>
        <p>Enter your tracking number to check your order status and updates</p>
      </div>

      {/* Tracking Form */}
      <div className="tracking-form-section">
        <form onSubmit={handleTrackOrder} className="tracking-form">
          <div className="input-group">
            <input
              type="text"
              value={trackingNumber}
              onChange={(e) => setTrackingNumber(e.target.value.toUpperCase())}
              placeholder="Enter your tracking number (e.g., FRE123ABC)"
              className="tracking-input"
              required
            />
            <button 
              type="submit" 
              disabled={loading} 
              className="track-button"
            >
              {loading ? (
                <>
                  <span className="spinner-small"></span>
                  Tracking...
                </>
              ) : (
                'Track Order'
              )}
            </button>
          </div>
        </form>

        {/* Recent Searches */}
        {recentSearches.length > 0 && (
          <div className="recent-searches">
            <p className="recent-title">Recent searches:</p>
            <div className="recent-tags">
              {recentSearches.map((search, index) => (
                <button
                  key={index}
                  className="recent-tag"
                  onClick={() => setTrackingNumber(search)}
                >
                  {search}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <div className="error-icon">❌</div>
          <div className="error-content">
            <h4>Order Not Found</h4>
            <p>{error}</p>
            <div className="error-suggestions">
              <p><strong>Please check:</strong></p>
              <ul>
                <li>Tracking number spelling</li>
                <li>Capital letters (FRE123ABC format)</li>
                <li>Order confirmation email</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Order Details */}
      {orderDetails && (
        <div className="order-details">
          {/* Order Header */}
          <div className="order-header">
            <div className="order-title">
              <h2>Order Tracking Details</h2>
              <p className="order-subtitle">Real-time updates for your order</p>
            </div>
            <div className="tracking-badge">
              <span className="badge-label">Tracking #</span>
              <span className="badge-value">{orderDetails.tracking_number}</span>
            </div>
          </div>

          {/* Current Status Card */}
          <div 
            className="status-card"
            style={{ borderLeftColor: getStatusColor(orderDetails.order_status) }}
          >
            <div className="status-header">
              <span className="status-icon">
                {getStatusIcon(orderDetails.order_status)}
              </span>
              <div className="status-info">
                <h3>Current Status: {orderDetails.status_display}</h3>
                <p>{getStatusDescription(orderDetails.order_status)}</p>
                <small>Last updated: {formatDate(new Date())}</small>
              </div>
            </div>
            <div className="status-progress">
              <div 
                className="progress-bar"
                style={{ 
                  width: `${(orderDetails.status_updates?.length / 5) * 100}%`,
                  backgroundColor: getStatusColor(orderDetails.order_status)
                }}
              ></div>
            </div>
          </div>

          {/* Order Information Grid */}
          <div className="order-info-grid">
            <div className="info-card">
              <h4>📦 Order Information</h4>
              <div className="info-content">
                <div className="info-row">
                  <span className="info-label">Customer Name:</span>
                  <span className="info-value">{orderDetails.customer_name}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Product Details:</span>
                  <span className="info-value">{orderDetails.product_details}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Order Date:</span>
                  <span className="info-value">{formatDate(orderDetails.order_date)}</span>
                </div>
              </div>
            </div>

            <div className="info-card">
              <h4>📞 Support Information</h4>
              <div className="info-content">
                <div className="info-row">
                  <span className="info-label">Email Support:</span>
                  <span className="info-value">{orderDetails.customer_support_email}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Phone Support:</span>
                  <span className="info-value">+255 123 456 789</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Support Hours:</span>
                  <span className="info-value">Mon-Fri 9AM-6PM EAT</span>
                </div>
              </div>
            </div>
          </div>

          {/* Order Timeline */}
          {orderDetails.status_updates && orderDetails.status_updates.length > 0 && (
            <div className="timeline-section">
              <h3>Order Timeline</h3>
              <p className="timeline-subtitle">Track your order's journey from placement to delivery</p>
              
              <div className="timeline">
                {orderDetails.status_updates.map((update, index) => (
                  <div key={index} className="timeline-item">
                    <div 
                      className="timeline-marker"
                      style={{ backgroundColor: getStatusColor(update.status) }}
                    >
                      {getStatusIcon(update.status)}
                    </div>
                    <div className="timeline-content">
                      <div className="timeline-header">
                        <h4>{update.status.replace('_', ' ').toUpperCase()}</h4>
                        <span className="timeline-date">
                          {formatDate(update.timestamp)}
                        </span>
                      </div>
                      <p className="timeline-description">
                        {update.notes || 'Status update recorded'}
                      </p>
                      {index === 0 && (
                        <div className="current-badge">Current</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Support Section */}
          <div className="support-section">
            <h4>Need Help With Your Order?</h4>
            <div className="support-options">
              <div className="support-option">
                <div className="support-icon">📧</div>
                <div className="support-info">
                  <h5>Email Support</h5>
                  <p>{orderDetails.customer_support_email}</p>
                  <small>Response within 24 hours</small>
                </div>
              </div>
              
              <div className="support-option">
                <div className="support-icon">📞</div>
                <div className="support-info">
                  <h5>Phone Support</h5>
                  <p>+255 123 456 789</p>
                  <small>Mon-Fri 9AM-6PM EAT</small>
                </div>
              </div>
              
              <div className="support-option">
                <div className="support-icon">💬</div>
                <div className="support-info">
                  <h5>Live Chat</h5>
                  <p>Available on website</p>
                  <small>Instant support</small>
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="action-buttons">
            <button 
              onClick={() => window.print()}
              className="btn btn-secondary"
            >
              📄 Print Details
            </button>
            <button 
              onClick={() => window.location.href = '/contact'}
              className="btn btn-primary"
            >
              📞 Contact Support
            </button>
          </div>
        </div>
      )}

      {/* How to Find Tracking Number */}
      {!orderDetails && !error && (
        <div className="help-section">
          <h3>Where to Find Your Tracking Number</h3>
          <div className="help-options">
            <div className="help-option">
              <div className="help-icon">📧</div>
              <div className="help-content">
                <h4>Order Confirmation Email</h4>
                <p>Check the email you received after placing your order</p>
              </div>
            </div>
            <div className="help-option">
              <div className="help-icon">📱</div>
              <div className="help-content">
                <h4>SMS Notification</h4>
                <p>Look for text messages from Frecha IoTech</p>
              </div>
            </div>
            <div className="help-option">
              <div className="help-icon">👤</div>
              <div className="help-content">
                <h4>Account Dashboard</h4>
                <p>Login to your account to view order history</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrderTracking;