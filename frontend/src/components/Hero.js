import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Compact Thinking Robots */}
        <div className="thinking-robots-container">
          {/* Left Robot */}
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

          {/* Center Content - More Compact */}
          <div className="hero-content">
            <h1>AI-Optimized Telecom</h1>
            <p>Smart solutions for Vodacom, Airtel, Yas, and Halotel</p>
            <a href="#order" className="btn">Get Connected</a>
          </div>

          {/* Right Robot */}
          <div className="thinking-robot robot-right">
            <div className="thinking-bubble">🤖</div>
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