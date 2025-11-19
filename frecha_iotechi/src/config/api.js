// src/config/api.js
const API_CONFIG = {
  // Development - local Django server
  development: {
    baseURL: 'http://localhost:8000/api',
    endpoints: {
      electronics: '/public-electronics/',
      routers: '/public-routers/',
      dataPlans: '/public-data-plans/',
      bundles: '/public-bundles/',
      createOrder: '/create-order/',
      trackOrder: '/track-order/'
    }
  },
  // Production - your Django server
  production: {
    baseURL: 'https://frecha-iotech.onrender.com/api',
    endpoints: {
      electronics: '/public-electronics/',
      routers: '/public-routers/',
      dataPlans: '/public-data-plans/',
      bundles: '/public-bundles/',
      createOrder: '/create-order/',
      trackOrder: '/track-order/'
    }
  }
};

// Get current environment
const environment = process.env.NODE_ENV || 'development';
const config = API_CONFIG[environment];

export default config;