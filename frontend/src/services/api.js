import axios from 'axios';

// Remove the fetch() call - just use the direct URL
const API_BASE_URL = 'https://frecha-iotech.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProviders = () => api.get('/api/providers/');
export const getBundles = () => api.get('/api/bundles/');
export const getBundlesByProvider = (providerId) => api.get(`/api/bundles/${providerId}/`);
export const getRouters = () => api.get('/api/routers/');
export const createOrder = (orderData) => api.post('/api/orders/', orderData);