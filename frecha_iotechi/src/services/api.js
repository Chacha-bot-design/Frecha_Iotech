import axios from 'axios';

const API_BASE_URL = 'https://frecha_iotech.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProviders = () => api.get('/providers/');
export const getBundles = () => api.get('/bundles/');
export const getBundlesByProvider = (providerId) => api.get(`/bundles-by-provider/${providerId}/`);
export const getRouters = () => api.get('/routers/');
export const createOrder = (orderData) => api.post('/orders/', orderData);
export const getOrders = () => api.get('/orders/');