// src/config/api.js
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://frecha-iotech.onrender.com' 
 
fetch('/api/providers/')
fetch('/api/bundles/') 
fetch('/api/orders/')

export default API_BASE_URL;