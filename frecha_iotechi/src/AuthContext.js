// src/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setUser(JSON.parse(userData));
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const signup = async (userData) => {
    try {
      const mockUser = {
        id: Date.now(),
        username: userData.username,
        email: userData.email
      };
      localStorage.setItem('user', JSON.stringify(mockUser));
      localStorage.setItem('token', 'mock-token');
      setUser(mockUser);
      setIsAuthenticated(true);
      return { success: true, user: mockUser };
    } catch (error) {
      return { success: false, message: 'Signup failed' };
    }
  };

  const login = async (credentials) => {
    try {
      const mockUser = {
        id: 1,
        username: credentials.username
      };
      localStorage.setItem('user', JSON.stringify(mockUser));
      localStorage.setItem('token', 'mock-token');
      setUser(mockUser);
      setIsAuthenticated(true);
      return { success: true, user: mockUser };
    } catch (error) {
      return { success: false, message: 'Login failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
  };

  const guestCheckout = async (orderData) => {
    return { success: true, data: orderData };
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    signup,
    login,
    logout,
    guestCheckout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;