// src/components/ProductList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import apiConfig from '../config/api';
import './ProductList.css';

const ProductList = ({ onAddToCart }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [apiStatus, setApiStatus] = useState('checking');

  const { baseURL, endpoints } = apiConfig;

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    setError(null);
    setApiStatus('fetching');
    
    try {
      console.log('Fetching from:', baseURL);
      
      // Use the correct endpoints from config
      const [electronicsRes, routersRes, dataPlansRes, bundlesRes] = await Promise.allSettled([
        axios.get(`${baseURL}${endpoints.electronics}`),
        axios.get(`${baseURL}${endpoints.routers}`),
        axios.get(`${baseURL}${endpoints.dataPlans}`),
        axios.get(`${baseURL}${endpoints.bundles}`)
      ]);

      console.log('API Responses:', { 
        electronics: electronicsRes,
        routers: routersRes,
        dataPlans: dataPlansRes,
        bundles: bundlesRes
      });

      const allProducts = [];

      // Process each response with better error handling
      const processResponse = (response, category, type, featureBase = []) => {
        if (response.status === 'fulfilled' && response.value && response.value.data) {
          const data = Array.isArray(response.value.data) ? response.value.data : [];
          return data.map(item => ({
            id: item.id || item.pk || Math.random(),
            name: item.name || 'Unnamed Product',
            category: category,
            description: item.description || `Premium ${category} from Frecha Iotech`,
            price: parseFloat(item.price) || 0,
            image: item.image || null,
            specifications: item.specifications,
            type: type,
            features: item.features || featureBase
          }));
        }
        return [];
      };

      allProducts.push(
        ...processResponse(electronicsRes, 'electronics', 'electronics', ['Electronics Device']),
        ...processResponse(routersRes, 'routers', 'router', ['Networking Equipment']),
        ...processResponse(dataPlansRes, 'data-plans', 'data-plan', ['Data Plan']),
        ...processResponse(bundlesRes, 'bundles', 'bundle', ['Bundle Package'])
      );

      // Filter out items with price 0
      const validProducts = allProducts.filter(item => item.price > 0);
      
      if (validProducts.length > 0) {
        setProducts(validProducts);
        setApiStatus('success');
        setError(null);
        console.log(`✅ Loaded ${validProducts.length} products from Django API`);
      } else {
        setApiStatus('no-data');
        setError('No products found in database. Using sample data.');
        setProducts(getSampleProducts());
        console.log('⚠️ No products from API, using sample data');
      }

    } catch (err) {
      console.error('❌ API Error:', err);
      setApiStatus('error');
      setError(`Cannot connect to server: ${err.message}. Using sample data.`);
      setProducts(getSampleProducts());
    } finally {
      setLoading(false);
    }
  };

  // Enhanced sample data
  const getSampleProducts = () => [
    {
      id: 1,
      name: "Fiber Optic Router",
      category: "routers",
      description: "High-speed fiber optic router for reliable internet connectivity",
      price: 299.99,
      image: null,
      type: "router",
      features: ["Gigabit speeds", "Dual-band WiFi", "4 Ethernet ports", "Advanced security"]
    },
    {
      id: 2,
      name: "4G Monthly Data Plan - 10GB",
      category: "data-plans",
      description: "Monthly 10GB data plan with unlimited night browsing",
      price: 25000,
      image: null,
      type: "data-plan",
      features: ["10GB High-speed", "30 days validity", "4G LTE", "Night bundle included"]
    },
    {
      id: 3,
      name: "Business Internet Bundle",
      category: "bundles",
      description: "Complete business solution with high-speed internet and priority support",
      price: 150000,
      image: null,
      type: "bundle",
      features: ["Unlimited data", "Priority support", "Static IP", "Business router", "99.9% uptime"]
    },
    {
      id: 4,
      name: "Wireless Access Point",
      category: "electronics",
      description: "Enterprise-grade wireless access point for extended coverage in large areas",
      price: 199.99,
      image: null,
      type: "electronics",
      features: ["300m range", "PoE support", "Multiple SSIDs", "Mesh capable"]
    },
    {
      id: 5,
      name: "Weekly Social Media Bundle",
      category: "data-plans",
      description: "7-day social media bundle for WhatsApp, Instagram, Facebook and Twitter",
      price: 5000,
      image: null,
      type: "data-plan",
      features: ["Social media apps", "7 days validity", "Unlimited usage", "Fast speeds"]
    },
    {
      id: 6,
      name: "Network Switch 8-Port",
      category: "electronics",
      description: "8-port gigabit network switch for small office and home networks",
      price: 89.99,
      image: null,
      type: "electronics",
      features: ["8 Gigabit ports", "Plug & play", "Compact design", "Energy efficient"]
    },
    {
      id: 7,
      name: "YouTube Streaming Bundle",
      category: "data-plans",
      description: "Special bundle optimized for YouTube streaming and video content",
      price: 15000,
      image: null,
      type: "data-plan",
      features: ["YouTube optimized", "30 days", "HD streaming", "No buffering"]
    },
    {
      id: 8,
      name: "5G WiFi Router",
      category: "routers",
      description: "Next-generation 5G WiFi router for ultra-fast internet speeds",
      price: 450.00,
      image: null,
      type: "router",
      features: ["5G ready", "WiFi 6", "Multi-user", "Smart connectivity"]
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

  const getApiStatusMessage = () => {
    switch (apiStatus) {
      case 'success': 
        return `Connected to Frecha Iotech (${products.length} products)`;
      case 'no-data': 
        return 'Database is empty. Showing demo products.';
      case 'error': 
        return `Server connection issue: ${error}`;
      case 'fetching': 
        return 'Connecting to Frecha Iotech server...';
      default: 
        return 'Initializing...';
    }
  };

  const getApiStatusIcon = () => {
    switch (apiStatus) {
      case 'success': return 'bi-check-circle-fill';
      case 'no-data': return 'bi-database-exclamation';
      case 'error': return 'bi-exclamation-triangle-fill';
      case 'fetching': return 'bi-arrow-repeat spin';
      default: return 'bi-hourglass-split';
    }
  };

  const getApiStatusColor = () => {
    switch (apiStatus) {
      case 'success': return 'success';
      case 'no-data': return 'warning';
      case 'error': return 'error';
      case 'fetching': return 'info';
      default: return 'info';
    }
  };

  if (loading) {
    return (
      <section className="products-section">
        <div className="container">
          <div className="products-loading">
            <i className="bi bi-arrow-repeat spin" style={{ fontSize: '3rem', marginBottom: '1rem' }}></i>
            <h3>Loading Frecha Iotech Products</h3>
            <p>{getApiStatusMessage()}</p>
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="products-section">
      <div className="container">
        <div className="products-header">
          <h1>Frecha Iotech Products & Services</h1>
          <p>Premium telecom equipment, data plans, and networking solutions across Tanzania</p>
        </div>

        {/* API Status Alert */}
        <div className={`api-alert ${getApiStatusColor()}`}>
          <i className={`bi ${getApiStatusIcon()}`}></i>
          <div className="alert-content">
            <strong>{getApiStatusMessage()}</strong>
            <small>Server: {baseURL}</small>
          </div>
          {(apiStatus === 'error' || apiStatus === 'no-data') && (
            <button 
              onClick={fetchProducts}
              className="retry-btn"
            >
              <i className="bi bi-arrow-clockwise"></i>
              Retry Connection
            </button>
          )}
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
              <span className="category-count">
                ({selectedCategory === 'all' || selectedCategory === category.id 
                  ? products.filter(p => p.category === category.id).length 
                  : 0})
              </span>
            </button>
          ))}
        </div>

        {/* Products Grid */}
        <div className="products-grid">
          {filteredProducts.length === 0 ? (
            <div className="products-empty">
              <i className="bi bi-search" style={{ fontSize: '3rem', marginBottom: '1rem', color: 'var(--gray-400)' }}></i>
              <h3>No Products in This Category</h3>
              <p>Try selecting a different category or check back later for new products.</p>
              <button 
                onClick={() => setSelectedCategory('all')}
                className="btn btn-primary"
              >
                <i className="bi bi-grid"></i>
                View All Products
              </button>
            </div>
          ) : (
            filteredProducts.map(product => (
              <div key={`${product.type}-${product.id}`} className="product-card">
                <div className="product-image-container">
                  {product.image ? (
                    <img 
                      src={product.image} 
                      alt={product.name}
                      className="product-image"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        const placeholder = e.target.nextSibling;
                        if (placeholder) placeholder.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div className={`product-image-placeholder ${product.image ? 'hidden' : ''}`}>
                    <i className={`bi ${getCategoryIcon(product.category)}`}></i>
                  </div>
                  <div className="product-badge">
                    {product.type.replace('-', ' ')}
                  </div>
                </div>
                
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
                        <span key={index} className="feature-tag">
                          <i className="bi bi-check"></i>
                          {feature}
                        </span>
                      ))}
                    </div>
                  )}
                  
                  <div className="product-price">
                    <span className="price-amount">TZS {product.price.toLocaleString()}</span>
                    {product.type === 'data-plan' && (
                      <span className="price-note">One-time purchase</span>
                    )}
                  </div>
                  
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
      </div>
    </section>
  );
};

export default ProductList;