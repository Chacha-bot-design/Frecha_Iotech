// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';
import MainApp from './components/MainApp';
import Footer from './components/Footer'; // Make sure this path is correct
import './App.css';


function App() {
  return (
    <AuthProvider>
      <Router>
        <MainApp />
        <Footer /> {/* Make sure Footer is used here */}
      </Router>
    </AuthProvider>
  );
}

export default App;