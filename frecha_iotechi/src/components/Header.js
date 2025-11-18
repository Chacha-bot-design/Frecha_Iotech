// src/components/Header.js
import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import './Header.css';

const Header = ({ cartItemsCount, currentView, onNavigate, onShowAuth }) => {
  const { isAuthenticated, user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = async () => {
    logout();
    onNavigate('products');
    setMobileMenuOpen(false);
  };

  const handleNavClick = (view) => {
    onNavigate(view);
    setMobileMenuOpen(false);
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          {/* Logo */}
        
<div 
  className="logo-container"
  onClick={() => onNavigate('products')}
>
  <div className="logo-svg">
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
      <circle cx="20" cy="20" r="18" fill="white" fillOpacity="0.1" stroke="white" strokeWidth="2"/>
      <path d="M20 8C13.3726 8 8 13.3726 8 20C8 26.6274 13.3726 32 20 32" stroke="white" strokeWidth="2" strokeLinecap="round"/>
      <path d="M20 12C15.5817 12 12 15.5817 12 20C12 24.4183 15.5817 28 20 28" stroke="white" strokeWidth="2" strokeLinecap="round"/>
      <circle cx="20" cy="20" r="4" fill="white"/>
    </svg>
  </div>
  <div className="logo-text">
    <span className="company-name blink">Frecha Iotech</span>
  </div>
</div>

          {/* Desktop Navigation */}
          <nav className="nav">
            <ul>
              <li>
                <button 
                  className={`nav-link ${currentView === 'products' ? 'active' : ''}`}
                  onClick={() => onNavigate('products')}
                >
                  <i className="bi bi-house"></i>
                  Home
                </button>
              </li>
              <li>
                <button className="nav-link">
                  <i className="bi bi-gear"></i>
                  Services
                </button>
              </li>
              <li>
                <button className="nav-link">
                  <i className="bi bi-grid"></i>
                  Products
                </button>
              </li>
              <li>
                <button 
                  className="nav-link"
                  onClick={() => onNavigate('cart')}
                >
                  <i className="bi bi-cart"></i>
                  Order
                </button>
              </li>
              <li>
                <button 
                  className="nav-link"
                  onClick={() => onNavigate('tracking')}
                >
                  <i className="bi bi-truck"></i>
                  Track Order
                </button>
              </li>
              
              {/* User Auth Section */}
              {isAuthenticated ? (
                <li className="user-menu">
                  <div className="dropdown">
                    <button className="dropdown-toggle">
                      <i className="bi bi-person-circle"></i>
                      {user?.username || user?.name || 'User'}
                    </button>
                    <div className="dropdown-content">
                      <button onClick={() => handleNavClick('profile')}>
                        <i className="bi bi-person"></i>
                        My Profile
                      </button>
                      <button onClick={() => handleNavClick('orders')}>
                        <i className="bi bi-bag-check"></i>
                        My Orders
                      </button>
                      <div className="dropdown-divider"></div>
                      <button 
                        onClick={handleLogout}
                        className="logout-link"
                      >
                        <i className="bi bi-box-arrow-right"></i>
                        Sign Out
                      </button>
                    </div>
                  </div>
                </li>
              ) : (
                <li>
                  <button 
                    className="auth-btn"
                    onClick={onShowAuth}
                  >
                    <i className="bi bi-person"></i>
                    Sign In
                  </button>
                </li>
              )}

              {/* Shopping Cart */}
              <li className="cart-icon">
                <button 
                  className="cart-btn"
                  onClick={() => onNavigate('cart')}
                >
                  <i className="bi bi-cart3"></i>
                  {cartItemsCount > 0 && (
                    <span className="cart-badge">{cartItemsCount}</span>
                  )}
                </button>
              </li>
            </ul>
          </nav>

          {/* Mobile Menu Button */}
          <button 
            className="mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <i className="bi bi-list" style={{ fontSize: '1.5rem' }}></i>
          </button>
        </div>

        {/* Mobile Menu */}
        <div className={`mobile-menu ${mobileMenuOpen ? 'open' : ''}`}>
          <nav className="mobile-nav">
            <button onClick={() => handleNavClick('products')}>
              <i className="bi bi-house"></i>Home
            </button>
            <button>
              <i className="bi bi-gear"></i>Services
            </button>
            <button>
              <i className="bi bi-grid"></i>Products
            </button>
            <button onClick={() => handleNavClick('cart')}>
              <i className="bi bi-cart"></i>Order
            </button>
            <button onClick={() => handleNavClick('tracking')}>
              <i className="bi bi-truck"></i>Track Order
            </button>
            
            {isAuthenticated ? (
              <>
                <button onClick={() => handleNavClick('profile')}>
                  <i className="bi bi-person"></i>My Profile
                </button>
                <button onClick={() => handleNavClick('orders')}>
                  <i className="bi bi-bag-check"></i>My Orders
                </button>
                <button onClick={handleLogout}>
                  <i className="bi bi-box-arrow-right"></i>Sign Out
                </button>
              </>
            ) : (
              <button onClick={onShowAuth}>
                <i className="bi bi-person"></i>Sign In
              </button>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;