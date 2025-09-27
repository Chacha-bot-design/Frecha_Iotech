import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Hero from './components/Hero';
import Services from './components/Services';
import Products from './components/Products';
import OrderForm from './components/OrderForm';
import Footer from './components/Footer';
import './App.css';

// Simple API service - no external file needed
const API_BASE = ''; // Same domain

const fetchData = async (endpoint) => {
  try {
    const response = await fetch(`${API_BASE}/api/${endpoint}/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    return [];
  }
};

function App() {
  const [providers, setProviders] = useState([]);
  const [bundles, setBundles] = useState([]);
  const [routers, setRouters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        console.log('Fetching data from API...');
        
        // Fetch all data in parallel
        const [providersData, bundlesData, routersData] = await Promise.all([
          fetchData('providers'),
          fetchData('bundles'),
          fetchData('routers')
        ]);
        
        console.log('Data fetched:', {
          providers: providersData,
          bundles: bundlesData, 
          routers: routersData
        });
        
        setProviders(Array.isArray(providersData) ? providersData : []);
        setBundles(Array.isArray(bundlesData) ? bundlesData : []);
        setRouters(Array.isArray(routersData) ? routersData : []);
        setLoading(false);
        
      } catch (err) {
        console.error('Error loading data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        flexDirection: 'column'
      }}>
        <h2>Loading Frecha Iotech...</h2>
        <p>Fetching data from server</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        flexDirection: 'column',
        color: 'red'
      }}>
        <h2>Error Loading App</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={
            <>
              <Hero />
              <Services providers={providers} />
              <Products routers={routers} />
              <OrderForm 
                providers={providers} 
                bundles={bundles} 
                routers={routers} 
              />
            </>
          } />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;