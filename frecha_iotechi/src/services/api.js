// services/api.js
import axios from 'axios';

const API_BASE_URL = 'https://frecha-iotech.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🔄 API Call: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Success: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Order functions
export const createOrder = async (orderData) => {
  const response = await api.post('/api/orders/create/', orderData);
  return response.data;
};

export const getBundlesByProvider = async (providerId) => {
  const response = await api.get(`/api/providers/${providerId}/bundles/`);
  return response.data;
};

export const trackOrder = async (trackingNumber) => {
  const response = await api.get(`/api/tracking/${trackingNumber}/`);
  return response.data;
};

// Data fetching functions
export const getProviders = async () => {
  const response = await api.get('/api/public/providers/');
  return response.data;
};

export const getBundles = async () => {
  const response = await api.get('/api/public/bundles/');
  return response.data;
};

export const getRouters = async () => {
  const response = await api.get('/api/public/routers/');
  return response.data;
};

export const getAllServices = async () => {
  const response = await api.get('/api/all-services/');
  return response.data;
};

export default api;