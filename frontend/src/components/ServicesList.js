import React, { useState, useEffect } from 'react';
import { getProviders } from '../services/api';
import OrderForm from './OrderForm';

const ServiceList = () => {
  const [providers, setProviders] = useState([]);
  const [bundles, setBundles] = useState([]);
  const [routers, setRouters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('🔄 Fetching data from API...');
        
        // Fetch providers
        const providersResponse = await getProviders();
        console.log('✅ Providers:', providersResponse.data);
        setProviders(providersResponse.data);
        
        // You'll need to add similar API calls for bundles and routers
        // const bundlesResponse = await getBundles();
        // setBundles(bundlesResponse.data);
        
        // const routersResponse = await getRouters();
        // setRouters(routersResponse.data);
        
      } catch (err) {
        console.error('❌ Error fetching data:', err);
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading services...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div>
      {/* Display providers list */}
      <section className="providers-section">
        <div className="container">
          <h2>Available Service Providers ({providers.length})</h2>
          <div className="providers-grid">
            {providers.map(provider => (
              <div key={provider.id} className="provider-card">
                <h3>{provider.name}</h3>
                <p>{provider.description || 'Telecom service provider'}</p>
                {provider.color && (
                  <div 
                    className="color-indicator" 
                    style={{ backgroundColor: provider.color }}
                  ></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pass providers to OrderForm */}
      <OrderForm 
        providers={providers} 
        bundles={bundles} 
        routers={routers} 
      />
    </div>
  );
};

export default ServiceList;