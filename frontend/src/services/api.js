import axios from 'axios';

const api = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to log outgoing requests
api.interceptors.request.use(
  (config) => {
    console.log(`🔄 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor to log responses
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Success: ${response.config.url}`, response.status);
    return response;
  },
  (error) => {
    console.error(`❌ API Error: ${error.config?.url}`, error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export const getProviders = () => api.get('/api/providers/');
export const getBundles = () => api.get('/api/bundles/');
export const getBundlesByProvider = (providerId) => api.get(`/api/bundles/provider/${providerId}/`);
export const getRouters = () => api.get('/api/routers/');
export const createOrder = (orderData) => api.post('/api/orders/', orderData);