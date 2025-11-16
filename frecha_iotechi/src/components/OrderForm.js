import React, { useState, useEffect } from 'react';
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

  const safeProviders = Array.isArray(providers) ? providers : [];
  const safeRouters = Array.isArray(routers) ? routers : [];
  const safeBundles = Array.isArray(bundles) ? bundles : [];

  useEffect(() => {
    console.log('=== ORDERFORM DEBUG ===');
    console.log('Providers:', safeProviders);
    console.log('Routers:', safeRouters);
    console.log('Selected provider:', selectedProvider);
    console.log('Filtered bundles:', filteredBundles);
    console.log('Form data:', formData);
    console.log('======================');
  }, [providers, routers, selectedProvider, filteredBundles, formData]);
const handleProviderChange = async (e) => {
  const providerId = e.target.value;
  setSelectedProvider(providerId);

  // Reset product_id when provider changes
  setFormData(prev => ({
    ...prev,
    product_id: ''
  }));

  if (providerId) {
    try {
      const response = await getBundlesByProvider(providerId);
      
      // ✅ CORRECTED: Extract bundles from the nested response structure
      const bundlesData = Array.isArray(response?.data?.bundles) 
        ? response.data.bundles 
        : [];
        
      setFilteredBundles(bundlesData);
      
      if (bundlesData.length === 0) {
        setMessage('No bundles available for this provider.');
      } else {
        setMessage('');
      }
    } catch (error) {
      console.error('Error fetching bundles:', error);
      setFilteredBundles([]);
      setMessage('Error loading bundles. Please try again.');
    }
  } else {
    setFilteredBundles([]);
    setMessage('');
  }
};
  // Helper function to get product details
  const getProductDetails = () => {
    if (formData.service_type === 'router' && formData.product_id) {
      const router = safeRouters.find(r => r.id === parseInt(formData.product_id));
      return router ? `Router: ${router.name} - TZS ${router.price}` : 'Router selected';
    } else if (formData.service_type === 'bundle' && formData.product_id) {
      const bundle = [...safeBundles, ...filteredBundles].find(b => b.id === parseInt(formData.product_id));
      return bundle ? `Bundle: ${bundle.name} - TZS ${bundle.price}` : 'Bundle selected';
    }
    return formData.package_details || 'No product details';
  };

  // Helper function to calculate total price
  const getTotalPrice = () => {
    if (formData.service_type === 'router' && formData.product_id) {
      const router = safeRouters.find(r => r.id === parseInt(formData.product_id));
      return router ? parseFloat(router.price) : 0.00;
    } else if (formData.service_type === 'bundle' && formData.product_id) {
      const bundle = [...safeBundles, ...filteredBundles].find(b => b.id === parseInt(formData.product_id));
      return bundle ? parseFloat(bundle.price) : 0.00;
    }
    return 0.00;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    try {
      // ✅ CORRECTED: Prepare data in the format your backend expects
      const submissionData = {
        customer_name: formData.customer_name,
        customer_email: formData.email,
        customer_phone: formData.phone,
        product_details: getProductDetails(),
        quantity: 1,
        total_price: getTotalPrice(),
        notes: formData.additional_notes || ''
      };

      console.log('Submitting to API:', submissionData);

      const response = await createOrder(submissionData);
      console.log('Order created successfully:', response);
      
      setMessage('Order placed successfully! We will contact you shortly.');

      // Reset form
      setFormData({
        customer_name: '',
        email: '',
        phone: '',
        service_type: '',
        product_id: '',
        package_details: '',
        additional_notes: ''
      });
      setSelectedProvider('');
      setFilteredBundles([]);

    } catch (error) {
      console.error('Order error:', error);
      let errorMessage = 'Error placing order. Please try again.';

      if (error?.response?.data) {
        const data = error.response.data;
        if (typeof data === 'string') {
          errorMessage = data;
        } else if (typeof data === 'object') {
          // Handle validation errors
          if (data.details) {
            errorMessage = data.details;
          } else {
            errorMessage = Object.values(data)
              .flat()
              .join(' | ');
          }
        }
      } else if (error?.message) {
        errorMessage = error.message;
      }

      setMessage(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="order-section" id="order">
      <div className="container">
        <h2 className="section-title">Place Your Order</h2>
        <div className="order-form">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="customer_name">Full Name</label>
              <input
                type="text"
                id="customer_name"
                name="customer_name"
                value={formData.customer_name}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="phone">Phone Number</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="service_type">Service Type</label>
              <select
                id="service_type"
                name="service_type"
                value={formData.service_type}
                onChange={handleInputChange}
                required
              >
                <option value="">Select Service Type</option>
                <option value="bundle">Data Bundle</option>
                <option value="router">Router</option>
              </select>
            </div>

            {formData.service_type === 'bundle' && (
              <>
                <div className="form-group">
                  <label htmlFor="provider">Provider</label>
                  <select
                    id="provider"
                    value={selectedProvider}
                    onChange={handleProviderChange}
                    required
                  >
                    <option value="">Select Provider</option>
                    {safeProviders.map(provider => (
                      <option key={provider.id} value={provider.id}>
                        {provider.name}
                      </option>
                    ))}
                  </select>
                </div>

                {selectedProvider && (
                  <div className="form-group">
                    <label htmlFor="product_id">Select Bundle</label>
                    <select
                      id="product_id"
                      name="product_id"
                      value={formData.product_id}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Bundle</option>
                      {filteredBundles.map(bundle => (
                        <option key={bundle.id} value={bundle.id}>
                          {bundle.name} - TZS {bundle.price}
                        </option>
                      ))}
                    </select>
                    {filteredBundles.length === 0 && (
                      <p style={{ color: '#666', fontSize: '14px' }}>
                        No bundles available for this provider
                      </p>
                    )}
                  </div>
                )}
              </>
            )}

            {formData.service_type === 'router' && (
              <div className="form-group">
                <label htmlFor="product_id">Select Router</label>
                <select
                  id="product_id"
                  name="product_id"
                  value={formData.product_id}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Router</option>
                  {safeRouters.map(router => (
                    <option key={router.id} value={router.id}>
                      {router.name} - TZS {router.price}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div className="form-group">
              <label htmlFor="package_details">Package Details (Optional)</label>
              <input
                type="text"
                id="package_details"
                name="package_details"
                value={formData.package_details}
                onChange={handleInputChange}
                placeholder="E.g., 10GB monthly bundle"
              />
            </div>

            <div className="form-group">
              <label htmlFor="additional_notes">Additional Notes</label>
              <textarea
                id="additional_notes"
                name="additional_notes"
                value={formData.additional_notes}
                onChange={handleInputChange}
                rows="4"
                placeholder="Any special requirements"
              ></textarea>
            </div>

            {/* Display order summary */}
            {(formData.product_id || formData.package_details) && (
              <div className="order-summary" style={{
                background: '#f8f9fa',
                padding: '15px',
                borderRadius: '5px',
                marginBottom: '20px',
                border: '1px solid #e9ecef'
              }}>
                <h4 style={{ margin: '0 0 10px 0' }}>Order Summary:</h4>
                <p style={{ margin: '5px 0' }}><strong>Product:</strong> {getProductDetails()}</p>
                <p style={{ margin: '5px 0' }}><strong>Total Price:</strong> TZS {getTotalPrice().toFixed(2)}</p>
              </div>
            )}

            <center>
              <button type="submit" className="btn" disabled={isSubmitting}>
                {isSubmitting ? 'Processing...' : 'Submit Order'}
              </button>
            </center>

            {message && (
              <div 
                className="message" 
                style={{
                  marginTop: '20px',
                  padding: '10px',
                  borderRadius: '5px',
                  backgroundColor: message.includes('success') ? '#d4edda' : '#f8d7da',
                  color: message.includes('success') ? '#155724' : '#721c24',
                  border: `1px solid ${message.includes('success') ? '#c3e6cb' : '#f5c6cb'}`
                }}
              >
                {message}
              </div>
            )}
          </form>
        </div>
      </div>
    </section>
  );
};

export default OrderForm;