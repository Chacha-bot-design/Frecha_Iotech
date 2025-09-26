const Hero = () => {
  return (
    <section className="hero" id="home">
      <div className="container">
        {/* Thinking Robot */}
        <div className="thinking-robot">
          <div className="thinking-dots">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
          <div className="robot-head">
            <div className="robot-face">
              <div className="robot-eyes">
                <div className="eye"></div>
                <div className="eye"></div>
              </div>
            </div>
          </div>
          <div className="robot-body"></div>
        </div>
        
        <h1>Premium Telecom Services & WiFi Solutions</h1>
        <p>Get the best Vodacom, Airtel, Yas, and Halotel bundles along with high-quality WiFi routers for seamless connectivity.</p>
        <a href="#order" className="btn">Order Now</a>
      </div>
    </section>
  );
};

export default Hero; 