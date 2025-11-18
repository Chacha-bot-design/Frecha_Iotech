// src/components/CheckoutForm.js
import React, { useState } from 'react';
import './CheckoutForm.css';

const CheckoutForm = ({ cartItems, total, onOrderSuccess, onBackToCart }) => {
  const [formData, setFormData] = useState({
    // Personal Information
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    
    // Shipping Address
    address: '',
    city: '',
    region: '',
    postalCode: '',
    
    // Payment
    paymentMethod: 'credit-card',
    
    // Additional
    notes: '',
    subscribe: false,
    terms: false
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate API call
    setTimeout(() => {
      const orderData = {
        id: 'ORD-' + Date.now(),
        items: cartItems,
        total: total + 10000 + total * 0.18, // shipping + tax
        customer: {
          name: `${formData.firstName} ${formData.lastName}`,
          email: formData.email,
          phone: formData.phone
        },
        shippingAddress: {
          address: formData.address,
          city: formData.city,
          region: formData.region,
          postalCode: formData.postalCode
        },
        orderDate: new Date().toISOString(),
        estimatedDelivery: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
      };

      setIsSubmitting(false);
      onOrderSuccess(orderData);
    }, 2000);
  };

  const shippingCost = 10000;
  const tax = total * 0.18;
  const finalTotal = total + shippingCost + tax;

  return (
    <section className="checkout-section">
      <div className="container">
        <div className="checkout-header">
          <h1>Checkout</h1>
          <p className="text-gray-600">Complete your order with secure payment</p>
        </div>

        <div className="checkout-content">
          <form onSubmit={handleSubmit} className="checkout-form">
            {/* Personal Information */}
            <div className="form-section">
              <h3 className="section-title">Personal Information</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">First Name *</label>
                  <input
                    type="text"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Last Name *</label>
                  <input
                    type="text"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                </div>
                <div className="form-group full-width">
                  <label className="form-label">Email Address *</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                </div>
                <div className="form-group full-width">
                  <label className="form-label">Phone Number *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Shipping Address */}
            <div className="form-section">
              <h3 className="section-title">Shipping Address</h3>
              <div className="form-grid">
                <div className="form-group full-width">
                  <label className="form-label">Street Address *</label>
                  <input
                    type="text"
                    name="address"
                    value={formData.address}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">City *</label>
                  <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Region *</label>
                  <select
                    name="region"
                    value={formData.region}
                    onChange={handleInputChange}
                    className="form-select"
                    required
                  >
                    <option value="">Select Region</option>
                    <option value="dar-es-salaam">Dar es Salaam</option>
                    <option value="arusha">Arusha</option>
                    <option value="dodoma">Dodoma</option>
                    <option value="mbeya">Mbeya</option>
                    <option value="mwanza">Mwanza</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Postal Code</label>
                  <input
                    type="text"
                    name="postalCode"
                    value={formData.postalCode}
                    onChange={handleInputChange}
                    className="form-input"
                  />
                </div>
              </div>
            </div>

            {/* Payment Method */}
            <div className="form-section">
              <h3 className="section-title">Payment Method</h3>
              <div className="payment-methods">
                <div className="payment-method">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="credit-card"
                    id="credit-card"
                    checked={formData.paymentMethod === 'credit-card'}
                    onChange={handleInputChange}
                    className="payment-radio"
                  />
                  <label htmlFor="credit-card" className="payment-label">
                    <i className="bi bi-credit-card payment-icon"></i>
                    <span>Credit Card</span>
                  </label>
                </div>
                <div className="payment-method">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="mobile-money"
                    id="mobile-money"
                    checked={formData.paymentMethod === 'mobile-money'}
                    onChange={handleInputChange}
                    className="payment-radio"
                  />
                  <label htmlFor="mobile-money" className="payment-label">
                    <i className="bi bi-phone payment-icon"></i>
                    <span>Mobile Money</span>
                  </label>
                </div>
                <div className="payment-method">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="bank-transfer"
                    id="bank-transfer"
                    checked={formData.paymentMethod === 'bank-transfer'}
                    onChange={handleInputChange}
                    className="payment-radio"
                  />
                  <label htmlFor="bank-transfer" className="payment-label">
                    <i className="bi bi-bank payment-icon"></i>
                    <span>Bank Transfer</span>
                  </label>
                </div>
              </div>
            </div>

            {/* Additional Information */}
            <div className="form-section">
              <h3 className="section-title">Additional Information</h3>
              <div className="form-group full-width">
                <label className="form-label">Order Notes</label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleInputChange}
                  className="form-textarea"
                  placeholder="Any special instructions for your order..."
                />
              </div>
              <div className="form-row">
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    name="subscribe"
                    id="subscribe"
                    checked={formData.subscribe}
                    onChange={handleInputChange}
                    className="checkbox-input"
                  />
                  <label htmlFor="subscribe" className="checkbox-label">
                    Subscribe to our newsletter
                  </label>
                </div>
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    name="terms"
                    id="terms"
                    checked={formData.terms}
                    onChange={handleInputChange}
                    className="checkbox-input"
                    required
                  />
                  <label htmlFor="terms" className="checkbox-label">
                    I agree to the terms and conditions *
                  </label>
                </div>
              </div>
            </div>

            <div className="form-actions">
              <button
                type="button"
                onClick={onBackToCart}
                className="back-btn"
              >
                <i className="bi bi-arrow-left"></i>
                Back to Cart
              </button>
              <button
                type="submit"
                disabled={isSubmitting || !formData.terms}
                className="submit-btn"
              >
                {isSubmitting ? (
                  <>
                    <i className="bi bi-arrow-repeat spin"></i>
                    Processing...
                  </>
                ) : (
                  <>
                    <i className="bi bi-lock-fill"></i>
                    Complete Order
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Order Summary */}
          <div className="order-summary">
            <h3 className="summary-title">Order Summary</h3>
            
            <div className="summary-items">
              {cartItems.map(item => (
                <div key={item.id} className="summary-item">
                  <div>
                    <div className="item-name">{item.name}</div>
                    <div className="item-quantity">Qty: {item.quantity}</div>
                  </div>
                  <div className="item-price">
                    TZS {(item.price * item.quantity).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>

            <div className="summary-totals">
              <div className="total-row">
                <span>Subtotal</span>
                <span>TZS {total.toLocaleString()}</span>
              </div>
              <div className="total-row">
                <span>Shipping</span>
                <span>TZS {shippingCost.toLocaleString()}</span>
              </div>
              <div className="total-row">
                <span>Tax (18%)</span>
                <span>TZS {tax.toLocaleString()}</span>
              </div>
              <div className="total-row final">
                <span>Total</span>
                <span className="final-total">TZS {finalTotal.toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CheckoutForm;