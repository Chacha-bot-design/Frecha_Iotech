import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Tesla-style Robots */}
        <div className="tesla-bots">
          <div className="tesla-bot"></div>
          <div className="tesla-bot"></div>
        </div>
        
        <h1>AI-Powered Telecom Solutions</h1>
        <p>Experience the future of connectivity with our intelligent telecom services and cutting-edge WiFi solutions powered by advanced robotics technology.</p>
        <a href="#order" className="btn">Get Connected</a>
      </div>
    </section>
  );
};

export default Hero;