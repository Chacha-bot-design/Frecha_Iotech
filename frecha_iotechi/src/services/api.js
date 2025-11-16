// services/api.js - CORRECTED VERSION
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://frecha-iotech.onrender.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to log outgoing requests
api.interceptors.request.use(
  (config) => {
    console.log(`🔄 API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
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

// ✅ CORRECT PUBLIC ROUTES
export const getProviders = () => api.get('/api/providers/');
export const getBundles = () => api.get('/api/bundles/');
export const getRouters = () => api.get('/api/routers/');
export const createOrder = (orderData) => api.post('/api/orders/create/', orderData);

// ✅ CORRECTED BUNDLES BY PROVIDER ROUTE - FIXED THIS LINE
export const getBundlesByProvider = (providerId) => 
  api.get(`/api/providers/${providerId}/bundles/`); // Removed '/public/' from the URL

// Test function
export const testAllEndpoints = async () => {
  try {
    console.log('🧪 Testing all API endpoints...');
    
    // Test providers
    const providers = await getProviders();
    console.log('✅ Providers endpoint:', providers.data);
    
    // Test bundles
    const bundles = await getBundles();
    console.log('✅ Bundles endpoint:', bundles.data);
    
    // Test routers
    const routers = await getRouters();
    console.log('✅ Routers endpoint:', routers.data);
    
    // Test bundles by provider
    if (providers.data && providers.data.length > 0) {
      const providerBundles = await getBundlesByProvider(providers.data[0].id);
      console.log('✅ Bundles by provider endpoint:', providerBundles.data);
    }
    
    console.log('🎉 All API endpoints are working!');
    return true;
  } catch (error) {
    console.error('❌ API test failed:', error);
    return false;
  }
};

export default api;