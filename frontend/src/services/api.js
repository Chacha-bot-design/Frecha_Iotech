import axios from 'axios';

const api = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor to handle different response structures
api.interceptors.response.use(
  (response) => {
    // If the response data is already an array, return it directly
    if (Array.isArray(response.data)) {
      return { data: response.data };
    }
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const getProviders = () => api.get('/api/providers/');
export const getBundles = () => api.get('/api/bundles/');
export const getBundlesByProvider = (providerId) => api.get(`/api/bundles/provider/${providerId}/`);
export const getRouters = () => api.get('/api/routers/');
export const createOrder = (orderData) => api.post('/api/orders/', orderData);