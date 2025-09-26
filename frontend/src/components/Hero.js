import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Two Robot Images */}
        <div className="robot-container">
          <img 
            src="https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" 
            alt="Humanoid Robot" 
            className="robot-image"
          />
          <img 
            src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" 
            alt="Tesla Optimus Robot" 
            className="robot-image"
          />
        </div>
        
        <div className="hero-content">
          <h1>Premium Telecom Services & WiFi Solutions</h1>
          <p>Get the best Vodacom, Airtel, Yas, and Halotel bundles along with high-quality WiFi routers for seamless connectivity.</p>
          <a href="#order" className="btn">Order Now</a>
        </div>
      </div>
    </section>
  );
};

export default Hero;