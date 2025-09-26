import React from 'react';

const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Ultra-Realistic Human Robots */}
        <div className="human-robots-container">
          {/* Left Robot - Human-like */}
          <div className="human-robot robot-left">
            <div className="robot-figure">
              <div className="robot-head">
                <div className="robot-face">
                  <div className="eyes-container">
                    <div className="eye"></div>
                    <div className="eye"></div>
                  </div>
                  <div className="mouth"></div>
                </div>
              </div>
              <div className="neck"></div>
              <div className="shoulders"></div>
              <div className="robot-body">
                <div className="arms">
                  <div className="arm arm-left">
                    <div className="hand"></div>
                  </div>
                  <div className="arm arm-right"></div>
                </div>
                <div className="legs">
                  <div className="leg">
                    <div className="foot"></div>
                  </div>
                  <div className="leg">
                    <div className="foot"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Center Content */}
          <div className="hero-content">
            <h1>Premium Telecom Services & WiFi Solutions</h1>
            <p>Get the best Vodacom, Airtel, Yas, and Halotel bundles along with high-quality WiFi routers for seamless connectivity</p>
            <a href="#order" className="btn">Connect With Future</a>
          </div>

          {/* Right Robot - Human-like */}
          <div className="human-robot robot-right">
            <div className="robot-figure">
              <div className="robot-head">
                <div className="robot-face">
                  <div className="eyes-container">
                    <div className="eye"></div>
                    <div className="eye"></div>
                  </div>
                  <div className="mouth"></div>
                </div>
              </div>
              <div className="neck"></div>
              <div className="shoulders"></div>
              <div className="robot-body">
                <div className="arms">
                  <div className="arm arm-left"></div>
                  <div className="arm arm-right">
                    <div className="hand"></div>
                  </div>
                </div>
                <div className="legs">
                  <div className="leg">
                    <div className="foot"></div>
                  </div>
                  <div className="leg">
                    <div className="foot"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;