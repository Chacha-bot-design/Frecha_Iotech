// src/components/Header.js
import React from 'react';
import { useAuth } from './AuthContext'; // Same directory
import './Header.css';

const Header = ({ cartItemsCount, currentView, onNavigate, onShowAuth }) => {
  const { isAuthenticated, user, logout } = useAuth();

  const handleLogout = async () => {
    logout(); // No await needed since it's synchronous in your AuthContext
    onNavigate('products');
  };

  return (
    <header className="header">
      <div className="container headerContent">
        {/* Logo */}
        <div 
          className="logo"
          onClick={() => onNavigate('products')}
        >
          <i className="bi bi-wifi"></i>
          Frecha Iotech
        </div>

        {/* Navigation */}
        <nav className="nav">
          <ul>
            <li>
              <a 
                href="#home" 
                onClick={(e) => {
                  e.preventDefault();
                  onNavigate('products');
                }}
                className={currentView === 'products' ? 'active' : ''}
              >
                <i className="bi bi-house"></i>
                Home
              </a>
            </li>
            <li>
              <a href="#services">
                <i className="bi bi-gear"></i>
                Services
              </a>
            </li>
            <li>
              <a href="#products">
                <i className="bi bi-grid"></i>
                Products
              </a>
            </li>
            <li>
              <a 
                href="#order"
                onClick={(e) => {
                  e.preventDefault();
                  onNavigate('cart');
                }}
              >
                <i className="bi bi-cart"></i>
                Order
              </a>
            </li>
            <li>
              <a 
                href="#track-order"
                onClick={(e) => {
                  e.preventDefault();
                  onNavigate('tracking');
                }}
              >
                <i className="bi bi-truck"></i>
                Track Order
              </a>
            </li>
            
            {/* User Profile / Auth */}
            {isAuthenticated ? (
              <li className="userMenu">
                <div className="dropdown">
                  <button className="dropdownToggle">
                    <i className="bi bi-person-circle"></i>
                    {user?.username || user?.name || 'User'}
                  </button>
                  <div className="dropdownContent">
                    <a 
                      href="#profile"
                      onClick={(e) => {
                        e.preventDefault();
                        onNavigate('profile');
                      }}
                    >
                      <i className="bi bi-person"></i>
                      My Profile
                    </a>
                    <a 
                      href="#orders"
                      onClick={(e) => {
                        e.preventDefault();
                        onNavigate('orders');
                      }}
                    >
                      <i className="bi bi-bag-check"></i>
                      My Orders
                    </a>
                    <div className="dropdownDivider"></div>
                    <a 
                      href="#logout"
                      onClick={(e) => {
                        e.preventDefault();
                        handleLogout();
                      }}
                      className="logoutLink"
                    >
                      <i className="bi bi-box-arrow-right"></i>
                      Sign Out
                    </a>
                  </div>
                </div>
              </li>
            ) : (
              <li>
                <button 
                  className="authBtn"
                  onClick={onShowAuth}
                >
                  <i className="bi bi-person"></i>
                  Sign In
                </button>
              </li>
            )}

            {/* Shopping Cart */}
            <li className="cartIcon">
              <button 
                className="cartBtn"
                onClick={() => onNavigate('cart')}
              >
                <i className="bi bi-cart3"></i>
                {cartItemsCount > 0 && (
                  <span className="cartBadge">{cartItemsCount}</span>
                )}
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;