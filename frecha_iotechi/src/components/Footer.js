// src/components/Footer.js
import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer id="contact">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>About Us</h3>
            <p>Frecha Iotech provides premium telecom services and networking solutions to individuals and businesses across Tanzania.</p>
          </div>
          
          <div className="footer-section">
            <h3>Contact Info</h3>
            <ul className="contact-info">
              <li><i className="bi bi-geo-alt"></i> Dodoma, Tanzania</li>
              <li><i className="bi bi-telephone"></i> +255 757 315 593</li>
              <li><i className="bi bi-envelope"></i> frechaiotech@gmail.com</li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h3>Follow Us</h3>
            <p>Stay connected with us on social media</p>
            <div className="social-links">
              <a href="https://www.facebook.com/frecha.iotech" target="_blank" rel="noopener noreferrer">
                <i className="bi bi-facebook"></i>
              </a>
              <a href="https://www.tiktok.com/@frecha_iotech" target="_blank" rel="noopener noreferrer">
                <i className="bi bi-tiktok"></i>
              </a>
              <a href="https://www.instagram.com/fret_ech" target="_blank" rel="noopener noreferrer">
                <i className="bi bi-instagram"></i>
              </a>
              <a href="https://wa.me/255757315593" target="_blank" rel="noopener noreferrer">
                <i className="bi bi-whatsapp"></i>
              </a>
            </div>
          </div>
        </div>
        
        <div className="copyright">
          <p>&copy; 2025 Frecha Iotech. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;