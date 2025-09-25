import React from 'react';

const Products = ({ routers }) => {
  return (
    <section className="container" id="products">
      <h2 className="section-title">Our Products</h2>
      <div className="products">
        {routers.map(router => (
          <div key={router.id} className="product-card">
            <div className="product-img">
              <i className="fas fa-wifi"></i>
            </div>
            <div className="product-content">
              <h3>{router.name}</h3>
              <p>{router.description}</p>
              <div className="price">TZS {router.price}</div>
              <a href="#order" className="btn">Order Now</a>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Products;