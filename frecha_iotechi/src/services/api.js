// src/api.js - UPDATE THESE URLS
import axios from 'axios';

const API_BASE = 'https://frecha-iotech.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

// ============ PUBLIC API CALLS ============
export const getProviders = () => 
  api.get('/public/providers/');  // CHANGED from '/providers/'

export const getBundles = () => 
  api.get('/public/bundles/');    // CHANGED from '/bundles/'

export const getRouters = () => 
  api.get('/public/routers/');    // CHANGED from '/routers/'

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