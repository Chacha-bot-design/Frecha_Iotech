// api.js - UPDATED with correct URLs
import axios from 'axios';

const API_BASE = 'https://frecha-iotech.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

// ============ PUBLIC API CALLS (No login required) ============
export const getPublicProviders = () => 
  api.get('/public/providers/');  // CHANGED: /public/providers/

export const getPublicBundles = () => 
  api.get('/public/bundles/');    // CHANGED: /public/bundles/

export const getPublicRouters = () => 
  api.get('/public/routers/');    // CHANGED: /public/routers/

export const getPublicStatus = () => 
  api.get('/public/status/');

export const submitContactForm = (data) => 
  api.post('/public/contact/', data);

// ============ PROTECTED API CALLS (Login required) ============
export const login = (username, password) => 
  api.post('/auth/login/', { username, password });

export const logout = () => 
  api.post('/auth/logout/');

export const getCurrentUser = () => 
  api.get('/auth/me/');

export const getProtectedProviders = () => 
  api.get('/protected/providers/');  // CHANGED: /protected/providers/

export const getProtectedBundles = () => 
  api.get('/protected/bundles/');    // CHANGED: /protected/bundles/

export const getProtectedRouters = () => 
  api.get('/protected/routers/');    // CHANGED: /protected/routers/

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      console.log('Authentication required for this feature');
    }
    return Promise.reject(error);
  }
);

export default api;