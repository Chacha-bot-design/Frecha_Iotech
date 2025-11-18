// src/components/ProductList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ProductList.css';

const ProductList = ({ onAddToCart }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Update this URL to match your Django API endpoint
  const API_BASE = 'https://frecha-iotech.onrender.com'; // Adjust to your Django server

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch data from your Django API
      const [electronicsRes, routersRes, dataPlansRes, bundlesRes] = await Promise.all([
        axios.get(`${API_BASE}/electronics-devices/`).catch(() => ({ data: [] })),
        axios.get(`${API_BASE}/router-products/`).catch(() => ({ data: [] })),
        axios.get(`${API_BASE}/data-plans/`).catch(() => ({ data: [] })),
        axios.get(`${API_BASE}/bundles/`).catch(() => ({ data: [] }))
      ]);

      // Transform Django data to frontend format
      const allProducts = [
        ...electronicsRes.data.map(item => ({
          id: item.id,
          name: item.name,
          category: 'electronics',
          description: item.description,
          price: parseFloat(item.price),
          image: item.image,
          specifications: item.specifications,
          type: 'electronics'
        })),
        ...routersRes.data.map(item => ({
          id: item.id,
          name: item.name,
          category: 'routers',
          description: item.description,
          price: parseFloat(item.price),
          image: item.image,
          specifications: item.specifications,
          type: 'router'
        })),
        ...dataPlansRes.data.map(item => ({
          id: item.id,
          name: item.name,
          category: 'data-plans',
          description: item.description || `${item.data_volume} - ${item.provider_name}`,
          price: parseFloat(item.price),
          image: null, // Data plans might not have images
          features: [`${item.data_volume}`, `${item.validity_days} days`, item.network_type],
          type: 'data-plan'
        })),
        ...bundlesRes.data.map(item => ({
          id: item.id,
          name: item.name,
          category: 'bundles',
          description: item.description,
          price: parseFloat(item.actual_price || item.total_price),
          image: null,
          features: item.features || [],
          type: 'bundle'
        }))
      ].filter(item => item.price > 0); // Only include items with price

      setProducts(allProducts);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError('Failed to load products. Please check if the Django server is running.');
      
      // Fallback to sample data if API is not available
      setProducts(getSampleProducts());
    } finally {
      setLoading(false);
    }
  };

  // Fallback sample data
  const getSampleProducts = () => [
    {
      id: 1,
      name: "Fiber Optic Router",
      category: "routers",
      description: "High-speed fiber optic router for reliable internet connectivity",
      price: 299.99,
      image: "/images/router.jpg",
      type: "router"
    },
    {
      id: 2,
      name: "4G Data Plan - 10GB",
      category: "data-plans",
      description: "Monthly 10GB data plan with unlimited night browsing",
      price: 25000,
      image: null,
      type: "data-plan"
    }
  ];

  const categories = [
    { id: 'all', name: 'All Products' },
    { id: 'electronics', name: 'Electronics' },
    { id: 'routers', name: 'Routers' },
    { id: 'data-plans', name: 'Data Plans' },
    { id: 'bundles', name: 'Bundles' }
  ];

  const filteredProducts = selectedCategory === 'all' 
    ? products 
    : products.filter(product => product.category === selectedCategory);

  const handleAddToCart = (product) => {
    onAddToCart(product);
    
    // Show success notification
    const event = new CustomEvent('cartNotification', { 
      detail: { 
        message: `${product.name} added to cart!`,
        type: 'success'
      }
    });
    window.dispatchEvent(event);
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'electronics': return 'bi-laptop';
      case 'routers': return 'bi-router';
      case 'data-plans': return 'bi-wifi';
      case 'bundles': return 'bi-box-seam';
      default: return 'bi-box';
    }
  };

  if (loading) {
    return (
      <section className="products-section">
        <div className="container">
          <div className="products-loading">
            <i className="bi bi-arrow-repeat spin" style={{ fontSize: '3rem', marginBottom: '1rem' }}></i>
            <h3>Loading Products from Database...</h3>
            <p>Fetching latest products from Frecha Iotech</p>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="products-section">
        <div className="container">
          <div className="products-empty">
            <i className="bi bi-exclamation-triangle" style={{ fontSize: '3rem', marginBottom: '1rem', color: 'var(--error)' }}></i>
            <h3>Connection Issue</h3>
            <p>{error}</p>
            <p style={{ fontSize: '0.9rem', color: 'var(--gray-600)', marginTop: '1rem' }}>
              Make sure your Django server is running on http://localhost:8000
            </p>
            <button 
              onClick={fetchProducts} 
              className="btn btn-primary"
              style={{ marginTop: '1rem' }}
            >
              <i className="bi bi-arrow-clockwise"></i>
              Try Again
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="products-section">
      <div className="container">
        <div className="products-header">
          <h1>Our Products & Services</h1>
          <p>Premium telecom equipment, data plans, and networking solutions across Tanzania</p>
        </div>

        {/* Category Filter */}
        <div className="category-filter">
          {categories.map(category => (
            <button
              key={category.id}
              className={`category-btn ${selectedCategory === category.id ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category.id)}
            >
              <i className={`bi ${getCategoryIcon(category.id)}`}></i>
              {category.name}
            </button>
          ))}
        </div>

        {/* Products Grid */}
        <div className="products-grid">
          {filteredProducts.length === 0 ? (
            <div className="products-empty">
              <i className="bi bi-inbox" style={{ fontSize: '3rem', marginBottom: '1rem', color: 'var(--gray-400)' }}></i>
              <h3>No Products Found</h3>
              <p>No products available in this category.</p>
            </div>
          ) : (
            filteredProducts.map(product => (
              <div key={`${product.type}-${product.id}`} className="product-card">
                {product.image ? (
                  <img 
                    src={product.image} 
                    alt={product.name}
                    className="product-image"
                    onError={(e) => {
                      e.target.src = '/images/placeholder.jpg';
                    }}
                  />
                ) : (
                  <div className="product-image-placeholder">
                    <i className={`bi ${getCategoryIcon(product.category)}`}></i>
                  </div>
                )}
                
                <div className="product-info">
                  <span className="product-category">
                    <i className={`bi ${getCategoryIcon(product.category)}`}></i>
                    {product.category.replace('-', ' ')}
                  </span>
                  
                  <h3 className="product-title">{product.name}</h3>
                  <p className="product-description">{product.description}</p>
                  
                  {product.features && product.features.length > 0 && (
                    <div className="product-features">
                      {product.features.slice(0, 3).map((feature, index) => (
                        <span key={index} className="feature-tag">{feature}</span>
                      ))}
                    </div>
                  )}
                  
                  <div className="product-price">TZS {product.price.toLocaleString()}</div>
                  
                  <div className="product-actions">
                    <button 
                      className="add-to-cart-btn"
                      onClick={() => handleAddToCart(product)}
                    >
                      <i className="bi bi-cart-plus"></i>
                      Add to Cart
                    </button>
                    <button className="view-details-btn">
                      <i className="bi bi-info-circle"></i>
                      Details
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* API Status Indicator */}
        <div className="api-status">
          <small style={{ color: 'var(--gray-500)' }}>
            <i className="bi bi-database"></i>
            Connected to Frecha Iotech Database
          </small>
        </div>
      </div>
    </section>
  );
};

export default ProductList;