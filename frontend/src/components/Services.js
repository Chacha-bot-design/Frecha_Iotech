import React from 'react';

const Services = ({ providers }) => {
  console.log('Services component - providers:', providers);
  
  if (!providers || providers.length === 0) {
    return (
      <section className="services">
        <div className="container">
          <h2>Service Providers</h2>
          <div style={{ 
            padding: '2rem', 
            textAlign: 'center', 
            background: '#f8f9fa',
            borderRadius: '8px',
            margin: '2rem 0'
          }}>
            <p>No service providers available at the moment.</p>
            <p>
              <a href="/admin" target="_blank" rel="noopener noreferrer">
                Add providers in Django admin
              </a>
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="services">
      <div className="container">
        <h2>Our Service Providers</h2>
        <div className="providers-grid">
          {providers.map(provider => (
            <div key={provider.id} className="provider-card">
              <h3>{provider.name}</h3>
              {provider.logo && (
                <img 
                  src={provider.logo} 
                  alt={provider.name}
                  style={{ maxWidth: '100px', height: 'auto' }}
                />
              )}
              <p>{provider.description}</p>
              <div 
                style={{ 
                  width: '30px', 
                  height: '30px', 
                  backgroundColor: provider.color,
                  borderRadius: '50%',
                  display: 'inline-block'
                }}
              ></div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;