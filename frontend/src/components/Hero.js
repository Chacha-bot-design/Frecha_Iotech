import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Real Humanoid Robot Images */}
        <div className="humanoid-robots">
          <img 
            src="https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" 
            alt="Tesla Optimus Robot" 
            className="humanoid-image"
          />
          <img 
            src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" 
            alt="Advanced Humanoid" 
            className="humanoid-image"
          />
          <img 
            src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" 
            alt="Human-like Android" 
            className="humanoid-image"
          />
        </div>
        
        <h1>Premium Telecom Services</h1>
        <p>Get the best Vodacom, Airtel, Yas, and Halotel bundles along with high-quality WiFi routers for seamless connectivity.</p>
        <a href="#order" className="btn">Connect with Future</a>
      </div>
    </section>
  );
};

export default Hero;