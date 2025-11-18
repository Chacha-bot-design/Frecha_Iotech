// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';
import MainApp from './components/MainApp';
import './App.css';
import './styles/bootstrap-icons.css'; // This should now work

function App() {
  return (
    <AuthProvider>
      <Router>
        <MainApp />
      </Router>
    </AuthProvider>
  );
}

export default App;