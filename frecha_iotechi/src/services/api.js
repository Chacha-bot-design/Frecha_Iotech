import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://frecha-iotech.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProviders = () => api.get('/providers/');
export const getBundles = () => api.get('/bundles/');
export const getBundlesByProvider = (providerId) => api.get(`/bundles/?provider_id=${providerId}`);
export const getRouters = () => api.get('/routers/');
export const createOrder = (orderData) => api.post('/orders/', orderData);
export const getOrders = () => api.get('/orders/');