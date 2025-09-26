import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { getProviders, getBundles, getRouters } from './services/api';
import Header from './components/Header';
import Hero from './components/Hero';
import Services from './components/Services';
import Products from './components/Products';
import OrderForm from './components/OrderForm';
import Footer from './components/Footer';
import './App.css';
import "bootstrap-icons/font/bootstrap-icons.css";

function App() {
  const [providers, setProviders] = useState([]);
  const [bundles, setBundles] = useState([]);
  const [routers, setRouters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [providersResponse, bundlesResponse, routersResponse] = await Promise.all([
          getProviders(),
          getBundles(),
          getRouters()
        ]);
        
        // Ensure we always set arrays, even if API returns undefined
        setProviders(Array.isArray(providersResponse?.data) ? providersResponse.data : []);
        setBundles(Array.isArray(bundlesResponse?.data) ? bundlesResponse.data : []);
        setRouters(Array.isArray(routersResponse?.data) ? routersResponse.data : []);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
        // Set empty arrays on error too
        setProviders([]);
        setBundles([]);
        setRouters([]);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

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