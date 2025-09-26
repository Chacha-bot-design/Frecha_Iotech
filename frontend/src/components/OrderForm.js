import React, { useState } from 'react';
import { createOrder, getBundlesByProvider } from '../services/api';

const OrderForm = ({ providers, bundles, routers }) => {
  const [formData, setFormData] = useState({
    customer_name: '',
    email: '',
    phone: '',
    service_type: '',
    product_id: '',
    package_details: '',
    additional_notes: ''
  });
  const [selectedProvider, setSelectedProvider] = useState('');
  const [filteredBundles, setFilteredBundles] = useState([]);
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Safe array fallbacks to prevent errors (REMOVE safeBundles since it's unused)
  const safeProviders = Array.isArray(providers) ? providers : [];
  const safeRouters = Array.isArray(routers) ? routers : [];
  // Remove this line: const safeBundles = Array.isArray(bundles) ? bundles : [];

  const handleProviderChange = async (e) => {
    const providerId = e.target.value;
    setSelectedProvider(providerId);
    
    if (providerId) {
      try {
        const response = await getBundlesByProvider(providerId);
        // Safe array check for API response
        setFilteredBundles(Array.isArray(response?.data) ? response.data : []);
      } catch (error) {
        console.error('Error fetching bundles:', error);
        setFilteredBundles([]);
      }
    } else {
      setFilteredBundles([]);
    }
  };

  // ... rest of your code remains the same ...
};

export default OrderForm;