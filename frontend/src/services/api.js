import axios from 'axios';

// Use empty baseURL for same-domain requests
const api = axios.create({
  baseURL: '', // This will make requests to the same domain as your React app
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProviders = () => api.get('/api/providers/');
export const getBundles = () => api.get('/api/bundles/');
export const getBundlesByProvider = (providerId) => api.get(`/api/bundles/provider/${providerId}/`);
export const getRouters = () => api.get('/api/routers/');
export const createOrder = (orderData) => api.post('/api/orders/', orderData);