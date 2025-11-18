// src/components/ShoppingCart.js
import React from 'react';
import './ShoppingCart.css';

const ShoppingCart = ({ 
  cartItems, 
  onUpdateQuantity, 
  onRemoveItem, 
  onProceedToCheckout 
}) => {
  const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const itemsCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  if (cartItems.length === 0) {
    return (
      <section className="cart-section">
        <div className="container">
          <div className="empty-cart">
            <i className="bi bi-cart-x"></i>
            <h3>Your cart is empty</h3>
            <p>Add some products to get started</p>
            <button 
              className="btn btn-primary"
              onClick={() => window.history.back()}
            >
              <i className="bi bi-arrow-left"></i>
              Continue Shopping
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="cart-section">
      <div className="container">
        <div className="cart-header">
          <h1>Shopping Cart</h1>
          <p className="text-gray-600">{itemsCount} {itemsCount === 1 ? 'item' : 'items'} in your cart</p>
        </div>

        <div className="cart-content">
          <div className="cart-items">
            {cartItems.map(item => (
              <div key={`${item.id}-${item.category}`} className="cart-item">
                <img 
                  src={item.image} 
                  alt={item.name}
                  className="cart-item-image"
                  onError={(e) => {
                    e.target.src = '/images/placeholder.jpg';
                  }}
                />
                <div className="cart-item-details">
                  <h3 className="cart-item-name">{item.name}</h3>
                  <div className="cart-item-category">{item.category}</div>
                  <div className="cart-item-price">
                    TZS {(item.price * item.quantity).toLocaleString()}
                  </div>
                  <div className="cart-item-actions">
                    <div className="quantity-controls">
                      <button 
                        className="quantity-btn"
                        onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                      >
                        <i className="bi bi-dash"></i>
                      </button>
                      <span className="quantity-display">{item.quantity}</span>
                      <button 
                        className="quantity-btn"
                        onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                      >
                        <i className="bi bi-plus"></i>
                      </button>
                    </div>
                    <button 
                      className="remove-btn"
                      onClick={() => onRemoveItem(item.id)}
                    >
                      <i className="bi bi-trash"></i>
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <h3 className="summary-title">Order Summary</h3>
            
            <div className="summary-row">
              <span>Items ({itemsCount})</span>
              <span>TZS {total.toLocaleString()}</span>
            </div>
            
            <div className="summary-row">
              <span>Shipping</span>
              <span>TZS 10,000</span>
            </div>
            
            <div className="summary-row">
              <span>Tax</span>
              <span>TZS {(total * 0.18).toLocaleString()}</span>
            </div>
            
            <div className="summary-row">
              <span>Total</span>
              <span className="summary-total">
                TZS {(total + 10000 + total * 0.18).toLocaleString()}
              </span>
            </div>

            <button 
              className="checkout-btn"
              onClick={onProceedToCheckout}
            >
              <i className="bi bi-lock-fill"></i>
              Proceed to Checkout
            </button>

            <button 
              className="continue-shopping btn btn-outline"
              onClick={() => window.history.back()}
            >
              <i className="bi bi-arrow-left"></i>
              Continue Shopping
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ShoppingCart;