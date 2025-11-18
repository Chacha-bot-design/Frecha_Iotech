// src/context/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function useAuth() {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing auth data
    const storedUser = localStorage.getItem('currentUser');
    const storedToken = localStorage.getItem('authToken');
    
    if (storedUser && storedToken) {
      try {
        setCurrentUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Error parsing stored user data:', error);
        localStorage.removeItem('currentUser');
        localStorage.removeItem('authToken');
      }
    }
    setLoading(false);
  }, []);

  const login = (userData, token) => {
    setCurrentUser(userData);
    localStorage.setItem('currentUser', JSON.stringify(userData));
    localStorage.setItem('authToken', token);
  };

  const logout = () => {
    setCurrentUser(null);
    localStorage.removeItem('currentUser');
    localStorage.removeItem('authToken');
  };

  const signup = (userData, token) => {
    setCurrentUser(userData);
    localStorage.setItem('currentUser', JSON.stringify(userData));
    localStorage.setItem('authToken', token);
  };

  const value = {
    currentUser,
    login,
    logout,
    signup,
    isAuthenticated: !!currentUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}