import React from 'react';

const Header = () => {
  return (
    <header>
      <div className="container header-content">
        <div className="logo">
          <i className="bi bi-wifi"></i>
          Frecha Iotech
        </div>
        <nav>
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#products">Products</a></li>
            <li><a href="#order">Order</a></li>
             <li><a href="/track-order">Track Order</li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;