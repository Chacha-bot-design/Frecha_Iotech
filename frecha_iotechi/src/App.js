import React, { useState, useEffect } from 'react';
import { getProviders, getBundles, getRouters } from './services/api';
import Header from './components/Header';
import Hero from './components/Hero';
import Services from './components/Services';
import Products from './components/Products';
import OrderForm from './components/OrderForm';
import Footer from './components/Footer';
import './App.css';

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
        
        setProviders(providersResponse.data);
        setBundles(bundlesResponse.data);
        setRouters(routersResponse.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="App">
      <Header />
      <Hero />
      <Services providers={providers} />
      <Products routers={routers} />
      <OrderForm providers={providers} bundles={bundles} routers={routers} />
      <Footer />
    </div>
  );
}

export default App;