import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';  // Django backend

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