import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        <div className="human-robots-container">
          
          {/* Male Robot Image */}
          <img 
            src="/images/Robot2.png"
            alt="Male Humanoid Robot" 
            className="human-robot-image male-bot"
            style={{
              width: '280px',
              height: '420px',
              objectFit: 'cover',
              borderRadius: '20px',
              border: '3px solid #00d4ff',
              boxShadow: '0 20px 40px rgba(0, 212, 255, 0.4)'
            }}
          />

          
          <div className="hero-content">
            <h1>Premium Telecom Services & WiFi Solutions</h1>
            <p>Get the best Vodacom, Airtel, Yas, and Halotel bundles along with high-quality WiFi routers for seamless connectivity.</p>
            <a href="#order" className="btn">Connect To Future</a>
          </div>

          {/* Male Robot Image */}
          <img 
            src="/images/Robot1.png"
            alt="Male Humanoid Robot" 
            className="human-robot-image male-bot"
            style={{
              width: '280px',
              height: '420px',
              objectFit: 'cover',
              borderRadius: '20px',
              border: '3px solid #00d4ff',
              boxShadow: '0 20px 40px rgba(0, 212, 255, 0.4)'
            }}
          />
        </div>
      </div>
    </section>
  );
};
export default Hero;
