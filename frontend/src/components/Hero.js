import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Real Human-like Robot Photos */}
        <div className="human-robots-container">
          <img 
            src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
            alt="Hyper-realistic female android" 
            className="human-robot-image"
            style={{
              width: '300px',
              height: '450px',
              objectFit: 'cover',
              borderRadius: '20px',
              border: '3px solid #00d4ff',
              boxShadow: '0 20px 40px rgba(0, 212, 255, 0.4)'
            }}
          />
          
          <div className="hero-content">
            <h1>Indistinguishable Human Robots</h1>
            <p>Advanced androids that look, move, and think like humans, delivering superior telecom experiences.</p>
            <a href="#order" className="btn">Meet Your AI Assistant</a>
          </div>

          <img 
            src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
            alt="Realistic male humanoid" 
            className="human-robot-image"
            style={{
              width: '300px',
              height: '450px',
              objectFit: 'cover',
              borderRadius: '20px',
              border: '3px solid #00ff88',
              boxShadow: '0 20px 40px rgba(0, 255, 136, 0.4)'
            }}
          />
        </div>
      </div>
    </section>
  );
};