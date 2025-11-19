// src/components/ProductList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ProductList.css';

const ProductList = ({ onAddToCart }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [apiStatus, setApiStatus] = useState('checking');

  // Use your actual Django API endpoints
  const API_BASE = 'https://frecha-iotech.onrender.com/api'; // For development
  // const API_BASE = 'https://your-django-domain.com/api'; // For production

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    setError(null);
    setApiStatus('fetching');
    
    try {
      // Use your actual Django API endpoints from urls.py
      const [electronicsRes, routersRes, dataPlansRes, bundlesRes] = await Promise.allSettled([
        axios.get(`${API_BASE}/public-electronics/`), // Matches your URL pattern
        axios.get(`${API_BASE}/public-routers/`),     // Matches your URL pattern
        axios.get(`${API_BASE}/public-data-plans/`),  // Matches your URL pattern
        axios.get(`${API_BASE}/public-bundles/`)      // Matches your URL pattern
      ]);

      console.log('API Responses:', { electronicsRes, routersRes, dataPlansRes, bundlesRes });

      const allProducts = [];

      // Process electronics
      if (electronicsRes.status === 'fulfilled' && electronicsRes.value.data) {
        const electronicsData = Array.isArray(electronicsRes.value.data) ? electronicsRes.value.data : [];
        allProducts.push(...electronicsData.map(item => ({
          id: item.id || item.pk,
          name: item.name,
          category: 'electronics',
          description: item.description,
          price: parseFloat(item.price) || 0,
          image: item.image,
          specifications: item.specifications,
          type: 'electronics',
          features: ['Electronics Device', 'Premium Quality']
        })));
      }

      // Process routers
      if (routersRes.status === 'fulfilled' && routersRes.value.data) {
        const routersData = Array.isArray(routersRes.value.data) ? routersRes.value.data : [];
        allProducts.push(...routersData.map(item => ({
          id: item.id || item.pk,
          name: item.name,
          category: 'routers',
          description: item.description,
          price: parseFloat(item.price) || 0,
          image: item.image,
          specifications: item.specifications,
          type: 'router',
          features: ['Networking', 'High Speed']
        })));
      }

      // Process data plans
      if (dataPlansRes.status === 'fulfilled' && dataPlansRes.value.data) {
        const dataPlansData = Array.isArray(dataPlansRes.value.data) ? dataPlansRes.value.data : [];
        allProducts.push(...dataPlansData.map(item => ({
          id: item.id || item.pk,
          name: item.name,
          category: 'data-plans',
          description: item.description || `${item.data_volume} - ${item.provider_name || 'Provider'}`,
          price: parseFloat(item.price) || 0,
          image: null,
          features: [
            item.data_volume,
            `${item.validity_days} days`,
            item.network_type,
            item.data_type
          ].filter(Boolean),
          type: 'data-plan'
        })));
      }

      // Process bundles
      if (bundlesRes.status === 'fulfilled' && bundlesRes.value.data) {
        const bundlesData = Array.isArray(bundlesRes.value.data) ? bundlesRes.value.data : [];
        allProducts.push(...bundlesData.map(item => ({
          id: item.id || item.pk,
          name: item.name,
          category: 'bundles',
          description: item.description,
          price: parseFloat(item.actual_price || item.total_price) || 0,
          image: null,
          features: item.features || [],
          type: 'bundle'
        })));
      }

      // Filter out items with price 0 and check if we got any products
      const validProducts = allProducts.filter(item => item.price > 0);
      
      if (validProducts.length > 0) {
        setProducts(validProducts);
        setApiStatus('success');
        setError(null);
        console.log(`Loaded ${validProducts.length} products from Django API`);
      } else {
        // If no products from API, use sample data
        setApiStatus('no-data');
        setError('No products found in database. Using sample data.');
        setProducts(getSampleProducts());
      }

    } catch (err) {
      console.error('Error fetching products:', err);
      setApiStatus('error');
      setError(`API Error: ${err.message}. Using sample data.`);
      setProducts(getSampleProducts());
    } finally {
      setLoading(false);
    }
  };

  // Enhanced sample data that matches your Django models
  const getSampleProducts = () => [
    {
      id: 1,
      name: "Fiber Optic Router",
      category: "routers",
      description: "High-speed fiber optic router for reliable internet connectivity",
      price: 299.99,
      image: null,
      type: "router",
      features: ["Gigabit speeds", "Dual-band WiFi", "4 Ethernet ports"]
    },
    {
      id: 2,
      name: "4G Monthly Data Plan - 10GB",
      category: "data-plans",
      description: "Monthly 10GB data plan with unlimited night browsing",
      price: 25000,
      image: null,
      type: "data-plan",
      features: ["10GB Data", "30 days validity", "4G LTE", "Night bundle"]
    },
    {
      id: 3,
      name: "Business Internet Bundle",
      category: "bundles",
      description: "Complete business solution with high-speed internet and support",
      price: 150000,
      image: null,
      type: "bundle",
      features: ["Unlimited data", "Priority support", "Static IP", "Business router"]
    },
    {
      id: 4,
      name: "Wireless Access Point",
      category: "electronics",
      description: "Enterprise-grade wireless access point for extended coverage",
      price: 199.99,
      image: null,
      type: "electronics",
      features: ["300m range", "PoE support", "Multiple SSIDs"]
    },
    {
      id: 5,
      name: "Weekly Social Media Bundle",
      category: "data-plans",
      description: "7-day social media bundle for WhatsApp, Instagram, and Facebook",
      price: 5000,
      image: null,
      type: "data-plan",
      features: ["Social media only", "7 days", "Unlimited apps"]
    },
    {
      id: 6,
      name: "Network Switch 8-Port",
      category: "electronics",
      description: "8-port gigabit network switch for small office networks",
      price: 89.99,
      image: null,
      type: "electronics",
      features: ["8 Gigabit ports", "Plug & play", "Compact design"]
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
      case 'success': return `Connected to Frecha Iotech API (${products.length} products loaded)`;
      case 'no-data': return 'No products in database. Showing sample data.';
      case 'error': return error;
      case 'fetching': return 'Connecting to Frecha Iotech API...';
      default: return 'Checking API connection...';
    }
  };

  const getApiStatusIcon = () => {
    switch (apiStatus) {
      case 'success': return 'bi-check-circle-fill';
      case 'no-data': return 'bi-info-circle-fill';
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
            <h3>Loading Products...</h3>
            <p>{getApiStatusMessage()}</p>
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

        {/* API Status Alert */}
        {apiStatus && (
          <div className={`api-alert ${getApiStatusColor()}`}>
            <i className={`bi ${getApiStatusIcon()}`}></i>
            <span>{getApiStatusMessage()}</span>
            {(apiStatus === 'error' || apiStatus === 'no-data') && (
              <button 
                onClick={fetchProducts}
                className="retry-btn"
              >
                <i className="bi bi-arrow-clockwise"></i>
                Retry
              </button>
            )}
          </div>
        )}

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
              <button 
                onClick={() => setSelectedCategory('all')}
                className="btn btn-outline"
              >
                View All Products
              </button>
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
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
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

        {/* Debug Info */}
        {process.env.NODE_ENV === 'development' && (
          <div className="debug-info">
            <details>
              <summary>API Debug Info</summary>
              <pre>
                API Base: {API_BASE}
                Status: {apiStatus}
                Products: {products.length}
                Endpoints Used:
                - {API_BASE}/public-electronics/
                - {API_BASE}/public-routers/
                - {API_BASE}/public-data-plans/
                - {API_BASE}/public-bundles/
              </pre>
            </details>
          </div>
        )}
      </div>
    </section>
  );
};

export default ProductList;