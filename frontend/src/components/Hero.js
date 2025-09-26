import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        <div className="human-robots-container">
          
          {/* Female Robot Image */}
          <img 
            src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
            alt="Female Humanoid Robot" 
            className="human-robot-image female-bot"
            style={{
              width: '280px',
              height: '420px',
              objectFit: 'cover',
              borderRadius: '20px',
              border: '3px solid #ff6b6b',
              boxShadow: '0 20px 40px rgba(255, 107, 107, 0.4)'
            }}
          />
          
          <div className="hero-content">
            <h1>Human-Like Robot Telecom Team</h1>
            <p>Our advanced female and male androids work together to provide seamless telecom services.</p>
            <a href="#order" className="btn">Meet Your AI Team</a>
          </div>

          {/* Male Robot Image */}
          <img 
            src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
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