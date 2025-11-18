// src/components/AuthModal.js
import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import './AuthModal.css';

const AuthModal = ({ isOpen, onClose, onSuccess, showGuestOption = true }) => {
  const { login, signup } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      let result;
      
      if (isLogin) {
        result = await login({
          email: formData.email,
          password: formData.password
        });
      } else {
        // Validation
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match');
          setLoading(false);
          return;
        }
        
        if (formData.password.length < 6) {
          setError('Password must be at least 6 characters long');
          setLoading(false);
          return;
        }

        result = await signup({
          name: formData.name,
          email: formData.email,
          password: formData.password
        });
      }

      if (result.success) {
        onSuccess();
        onClose();
        // Reset form
        setFormData({
          name: '',
          email: '',
          password: '',
          confirmPassword: ''
        });
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGuestCheckout = () => {
    onSuccess();
    onClose();
  };

  const handleSocialLogin = (provider) => {
    // In a real app, this would redirect to OAuth provider
    setError(`${provider} login will be available soon!`);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <button className="close-btn" onClick={onClose}>
            <i className="bi bi-x-lg"></i>
          </button>
          <h2 className="modal-title">
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h2>
          <p className="modal-subtitle">
            {isLogin ? 'Sign in to your account' : 'Join Frecha Iotech today'}
          </p>
        </div>

        {/* Body */}
        <div className="modal-body">
          <form onSubmit={handleSubmit} className="auth-form">
            {!isLogin && (
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="form-input"
                  required
                  placeholder="Enter your full name"
                />
              </div>
            )}
            
            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="form-input"
                required
                placeholder="Enter your email"
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="form-input"
                required
                placeholder="Enter your password"
                minLength="6"
              />
            </div>
            
            {!isLogin && (
              <div className="form-group">
                <label className="form-label">Confirm Password</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="form-input"
                  required
                  placeholder="Confirm your password"
                  minLength="6"
                />
              </div>
            )}
            
            {error && (
              <div className="error-message">
                <i className="bi bi-exclamation-circle"></i> {error}
              </div>
            )}
            
            <button 
              type="submit" 
              className="submit-btn" 
              disabled={loading}
            >
              {loading ? (
                <>
                  <i className="bi bi-arrow-repeat spin"></i>
                  {isLogin ? 'Signing In...' : 'Creating Account...'}
                </>
              ) : (
                <>
                  <i className={isLogin ? 'bi bi-box-arrow-in-right' : 'bi bi-person-plus'}></i>
                  {isLogin ? 'Sign In' : 'Create Account'}
                </>
              )}
            </button>
          </form>

          {/* Social Login */}
          {isLogin && (
            <div className="social-auth">
              <div className="social-divider">
                <span>Or continue with</span>
              </div>
              <div className="social-buttons">
                <button 
                  className="social-btn google"
                  onClick={() => handleSocialLogin('Google')}
                  type="button"
                >
                  <i className="bi bi-google"></i>
                  Google
                </button>
                <button 
                  className="social-btn facebook"
                  onClick={() => handleSocialLogin('Facebook')}
                  type="button"
                >
                  <i className="bi bi-facebook"></i>
                  Facebook
                </button>
              </div>
            </div>
          )}

          {/* Switch between Login/Signup */}
          <div className="auth-switch">
            <button 
              type="button"
              className="switch-btn"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
            </button>
          </div>

          {/* Guest Checkout Option */}
          {showGuestOption && isLogin && (
            <div className="guest-option">
              <button 
                type="button"
                className="guest-btn"
                onClick={handleGuestCheckout}
              >
                <i className="bi bi-cart"></i>
                Continue as Guest
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthModal;