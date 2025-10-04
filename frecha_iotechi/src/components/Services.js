import React from 'react';

const Services = ({ providers }) => {
  return (
    <section className="container" id="services">
      <h2 className="section-title">Our Services</h2>
      <div className="services">
        {providers.map(provider => (
          <div key={provider.id} className="service-card">
            <div className="service-img" style={{ backgroundColor: provider.color }}>
              <i className={provider.logo}></i>
            </div>
            <div className="service-content">
              <h3>{provider.name} Bundles</h3>
              <p>High-quality data bundles with extensive coverage.</p>
              <div className="price">From TZS 10,000</div>
              <a href="#order" className="btn">Order Now</a>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Services;