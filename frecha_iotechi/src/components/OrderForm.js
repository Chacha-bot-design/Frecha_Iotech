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
        const bundlesData = Array.isArray(response?.data) ? response.data : [];
        setFilteredBundles(bundlesData);
      } catch (error) {
        console.error('Error fetching bundles:', error);
        setFilteredBundles([]);
        setMessage('Error loading bundles. Please try again.');
      }
    } else {
      setFilteredBundles([]);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // ✅ Ensure product_id is a number, or null if empty
      const submissionData = {
        ...formData,
        product_id: formData.product_id ? Number(formData.product_id) : null
      };

      console.log('Submitting to API:', submissionData);

      await createOrder(submissionData);
      setMessage('Order placed successfully!');

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
          errorMessage = Object.values(data)
            .flat()
            .join(' | ');
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
              <label htmlFor="package_details">Package Details</label>
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

            <center>
              <button type="submit" className="btn" disabled={isSubmitting}>
                {isSubmitting ? 'Processing...' : 'Submit Order'}
              </button>
            </center>

            {message && <div className="message">{message}</div>}
          </form>
        </div>
      </div>
    </section>
  );
};

export default OrderForm;
