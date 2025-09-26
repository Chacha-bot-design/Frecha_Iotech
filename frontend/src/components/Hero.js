import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Two Thinking Humanoid Robots */}
        <div className="thinking-robots-container">
          {/* Left Robot - Hand on Chin Thinking Pose */}
          <div className="thinking-robot robot-left">
            <div className="thinking-bubble">💭</div>
            <div className="robot-head">
              <div className="robot-face">
                <div className="eye"></div>
                <div className="eye"></div>
              </div>
            </div>
            <div className="robot-body">
              <div className="robot-arms">
                <div className="arm arm-left">
                  <div className="hand"></div>
                </div>
                <div className="arm arm-right"></div>
              </div>
              <div className="robot-legs">
                <div className="leg"></div>
                <div className="leg"></div>
              </div>
            </div>
          </div>

          {/* Center Content */}
          <div className="hero-content">
            <h1>AI Robots Thinking About Your Connectivity</h1>
            <p>Our advanced humanoid AI is constantly optimizing the best telecom solutions for your Vodacom, Airtel, Yas, and Halotel needs.</p>
            <a href="#order" className="btn">Get AI-Optimized Service</a>
          </div>

          {/* Right Robot - Hand on Head Thinking Pose */}
          <div className="thinking-robot robot-right">
            <div className="thinking-bubble">🤔</div>
            <div className="robot-head">
              <div className="robot-face">
                <div className="eye"></div>
                <div className="eye"></div>
              </div>
            </div>
            <div className="robot-body">
              <div className="robot-arms">
                <div className="arm arm-left"></div>
                <div className="arm arm-right">
                  <div className="hand"></div>
                </div>
              </div>
              <div className="robot-legs">
                <div className="leg"></div>
                <div className="leg"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;