import React from 'react';
import { useAuth } from '../context/AuthContext';
import styles from './Header.module.css';

const Header = ({ cartItemsCount, currentView, onNavigate, onShowAuth }) => {
  const { isAuthenticated, user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    onNavigate('products');
  };

  return (
    <header className={styles.header}>
      <div className={`container ${styles.headerContent}`}>
        {/* Logo */}
        <div 
          className={styles.logo}
          onClick={() => onNavigate('products')}
        >
          <i className="bi bi-wifi"></i>
          Frecha Iotech
        </div>

        {/* Navigation */}
        <nav className={styles.nav}>
          <ul>
            <li>
              <a 
                href="#home" 
                onClick={(e) => {
                  e.preventDefault();
                  onNavigate('products');
                }}
                className={currentView === 'products' ? styles.active : ''}
              >
                Home
              </a>
            </li>
            <li><a href="#services">Services</a></li>
            <li><a href="#products">Products</a></li>
            <li>
              <a 
                href="#order"
                onClick={(e) => {
                  e.preventDefault();
                  onNavigate('cart');
                }}
              >
                Order
              </a>
            </li>
            <li>
              <a 
                href="/track-order"
                onClick={(e) => {
                  e.preventDefault();
                  onNavigate('tracking');
                }}
              >
                Track Order
              </a>
            </li>
            
            {/* User Profile / Auth */}
            {isAuthenticated ? (
              <li className={styles.userMenu}>
                <div className={styles.dropdown}>
                  <button className={styles.dropdownToggle}>
                    <i className="bi bi-person-circle"></i>
                    {user?.username}
                  </button>
                  <div className={styles.dropdownContent}>
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
                        onNavigate('profile');
                      }}
                    >
                      <i className="bi bi-bag-check"></i>
                      My Orders
                    </a>
                    <div className={styles.dropdownDivider}></div>
                    <a 
                      href="#logout"
                      onClick={(e) => {
                        e.preventDefault();
                        handleLogout();
                      }}
                      className={styles.logoutLink}
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
                  className={styles.authBtn}
                  onClick={onShowAuth}
                >
                  <i className="bi bi-person"></i>
                  Sign In
                </button>
              </li>
            )}

            {/* Shopping Cart */}
            <li className={styles.cartIcon}>
              <button 
                className={styles.cartBtn}
                onClick={() => onNavigate('cart')}
              >
                <i className="bi bi-cart3"></i>
                {cartItemsCount > 0 && (
                  <span className={styles.cartBadge}>{cartItemsCount}</span>
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