// frecha_iotechi/src/api.js - UPDATE THIS FILE
import axios from 'axios';

const API_BASE = 'https://frecha-iotech.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

// ============ PUBLIC API CALLS ============
export const getProviders = () => 
  api.get('/public/providers/');  // CHANGED: added /public/

export const getBundles = () => 
  api.get('/public/bundles/');    // CHANGED: added /public/

export const getRouters = () => 
  api.get('/public/routers/');    // CHANGED: added /public/

export const getPublicStatus = () => 
  api.get('/public/status/');

export const submitContactForm = (data) => 
  api.post('/public/contact/', data);

// ============ AUTHENTICATION ============
export const login = (username, password) => 
  api.post('/auth/login/', { username, password });

export const logout = () => 
  api.post('/auth/logout/');

export const getCurrentUser = () => 
  api.get('/auth/me/');

export default api;