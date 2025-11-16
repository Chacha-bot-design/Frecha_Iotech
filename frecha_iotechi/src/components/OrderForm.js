import React, { useState, useEffect } from 'react';
import { createOrder, getBundlesByProvider } from '../services/api';
import './OrderForm.css'; // We'll create this CSS file

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
  const [isLoadingBundles, setIsLoadingBundles] = useState(false);
  const [orderResult, setOrderResult] = useState(null);

  const safeProviders = Array.isArray(providers) ? providers : [];
  const safeRouters = Array.isArray(routers) ? routers : [];
  const safeBundles = Array.isArray(bundles) ? bundles : [];

  // Debug logging
  useEffect(() => {
    console.log('=== ORDERFORM DEBUG ===');
    console.log('Providers:', safeProviders.length);
    console.log('Routers:', safeRouters.length);
    console.log('Bundles:', safeBundles.length);
    console.log('Selected provider:', selectedProvider);
    console.log('Filtered bundles:', filteredBundles.length);
    console.log('======================');
  }, [providers, routers, selectedProvider, filteredBundles]);

  // Handle provider change and fetch bundles
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
        setIsLoadingBundles(true);
        setMessage('🔄 Loading bundles...');

        const response = await getBundlesByProvider(providerId);
        
        // Handle different response structures
        let bundlesData = [];
        
        if (Array.isArray(response)) {
          bundlesData = response;
        } else if (Array.isArray(response?.bundles)) {
          bundlesData = response.bundles;
        } else if (Array.isArray(response?.data?.bundles)) {
          bundlesData = response.data.bundles;
        } else if (Array.isArray(response?.data)) {
          bundlesData = response.data;
        }
        
        setFilteredBundles(bundlesData);
        
        if (bundlesData.length === 0) {
          setMessage('ℹ️ No bundles available for this provider.');
        } else {
          setMessage(`✅ Found ${bundlesData.length} bundle(s)`);
          setTimeout(() => setMessage(''), 2000);
        }
      } catch (error) {
        console.error('Error fetching bundles:', error);
        setFilteredBundles([]);
        setMessage('❌ Error loading bundles. Please try again.');
      } finally {
        setIsLoadingBundles(false);
      }
    } else {
      setFilteredBundles([]);
      setMessage('');
    }
  };

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Get product details for display
  const getProductDetails = () => {
    if (formData.service_type === 'router' && formData.product_id) {
      const router = safeRouters.find(r => r.id === parseInt(formData.product_id));
      return router ? `${router.name} - TZS ${router.price}` : 'Router selected';
    } else if (formData.service_type === 'bundle' && formData.product_id) {
      const bundle = [...safeBundles, ...filteredBundles].find(b => b.id === parseInt(formData.product_id));
      return bundle ? `${bundle.name} - TZS ${bundle.price}` : 'Bundle selected';
    }
    return formData.package_details || 'Custom order';
  };

  // Calculate total price
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

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');
    setOrderResult(null);

    try {
      // Prepare data for backend
      const submissionData = {
        customer_name: formData.customer_name,
        customer_email: formData.email,
        customer_phone: formData.phone,
        product_details: getProductDetails(),
        quantity: 1,
        total_price: getTotalPrice(),
        notes: formData.additional_notes || ''
      };

      console.log('Submitting order:', submissionData);

      const response = await createOrder(submissionData);
      console.log('Order response:', response);
      
      // Handle successful order with tracking
      if (response.success) {
        setOrderResult({
          orderId: response.order.id,
          trackingNumber: response.tracking_number,
          customerName: response.order.customer_name,
          totalPrice: response.order.total_price,
          status: response.order.status
        });
        
        setMessage(`✅ Order placed successfully! Tracking Number: ${response.tracking_number}`);
        
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
      } else {
        throw new Error(response.message || 'Order failed');
      }

    } catch (error) {
      console.error('Order error:', error);
      let errorMessage = '❌ Error placing order. Please try again.';

      if (error?.response?.data) {
        const data = error.response.data;
        if (typeof data === 'string') {
          errorMessage = `❌ ${data}`;
        } else if (typeof data === 'object') {
          if (data.details) {
            errorMessage = `❌ ${data.details}`;
          } else if (data.error) {
            errorMessage = `❌ ${data.error}`;
          } else {
            errorMessage = `❌ ${Object.values(data).flat().join(' | ')}`;
          }
        }
      } else if (error?.message) {
        errorMessage = `❌ ${error.message}`;
      }

      setMessage(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Reset form for new order
  const handleNewOrder = () => {
    setOrderResult(null);
    setMessage('');
  };

  // If we have order result, show success page
  if (orderResult) {
    return (
      <section className="order-section" id="order">
        <div className="container">
          <div className="order-success">
            <div className="success-icon">🎉</div>
            <h2>Order Placed Successfully!</h2>
            <p>Thank you for your order. We'll process it within 24 hours.</p>
            
            <div className="order-details-card">
              <h3>Order Details</h3>
              <div className="detail-row">
                <span className="label">Order ID:</span>
                <span className="value">#{orderResult.orderId}</span>
              </div>
              <div className="detail-row">
                <span className="label">Tracking Number:</span>
                <span className="value tracking-number">{orderResult.trackingNumber}</span>
              </div>
              <div className="detail-row">
                <span className="label">Customer:</span>
                <span className="value">{orderResult.customerName}</span>
              </div>
              <div className="detail-row">
                <span className="label">Total Amount:</span>
                <span className="value">TZS {orderResult.totalPrice}</span>
              </div>
              <div className="detail-row">
                <span className="label">Status:</span>
                <span className="value status-badge">{orderResult.status}</span>
              </div>
            </div>

            <div className="next-steps">
              <h4>What's Next?</h4>
              <ul>
                <li>📧 You'll receive an order confirmation email</li>
                <li>📦 We'll process your order within 24 hours</li>
                <li>🚚 You'll receive shipping updates</li>
                <li>🔍 Use your tracking number to monitor progress</li>
              </ul>
            </div>

            <div className="action-buttons">
              <button 
                onClick={() => window.location.href = `/track-order?tracking=${orderResult.trackingNumber}`}
                className="btn btn-primary"
              >
                Track Your Order
              </button>
              <button 
                onClick={handleNewOrder}
                className="btn btn-secondary"
              >
                Place Another Order
              </button>
            </div>
          </div>
        </div>
      </section>
    );
  }

  // Main order form
  return (
    <section className="order-section" id="order">
      <div className="container">
        <h2 className="section-title">Place Your Order</h2>
        <p className="section-subtitle">Fill out the form below to place your order</p>
        
        <div className="order-form-container">
          <form onSubmit={handleSubmit} className="order-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="customer_name" className="form-label">
                  Full Name *
                </label>
                <input
                  type="text"
                  id="customer_name"
                  name="customer_name"
                  value={formData.customer_name}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="email" className="form-label">
                  Email Address *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Enter your email"
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="phone" className="form-label">
                  Phone Number *
                </label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Enter your phone number"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="service_type" className="form-label">
                  Service Type *
                </label>
                <select
                  id="service_type"
                  name="service_type"
                  value={formData.service_type}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                >
                  <option value="">Select Service Type</option>
                  <option value="bundle">Data Bundle</option>
                  <option value="router">Router</option>
                </select>
              </div>
            </div>

            {formData.service_type === 'bundle' && (
              <>
                <div className="form-group">
                  <label htmlFor="provider" className="form-label">
                    Internet Provider *
                  </label>
                  <select
                    id="provider"
                    value={selectedProvider}
                    onChange={handleProviderChange}
                    className="form-select"
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
                    <label htmlFor="product_id" className="form-label">
                      Select Data Bundle *
                    </label>
                    <select
                      id="product_id"
                      name="product_id"
                      value={formData.product_id}
                      onChange={handleInputChange}
                      className="form-select"
                      required
                      disabled={isLoadingBundles}
                    >
                      <option value="">
                        {isLoadingBundles ? 'Loading bundles...' : 'Select Bundle'}
                      </option>
                      {filteredBundles.map(bundle => (
                        <option key={bundle.id} value={bundle.id}>
                          {bundle.name} - {bundle.data_volume} - TZS {bundle.price}
                        </option>
                      ))}
                    </select>
                    {filteredBundles.length === 0 && !isLoadingBundles && (
                      <p className="no-bundles-message">
                        No bundles available for this provider
                      </p>
                    )}
                  </div>
                )}
              </>
            )}

            {formData.service_type === 'router' && (
              <div className="form-group">
                <label htmlFor="product_id" className="form-label">
                  Select Router *
                </label>
                <select
                  id="product_id"
                  name="product_id"
                  value={formData.product_id}
                  onChange={handleInputChange}
                  className="form-select"
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
              <label htmlFor="package_details" className="form-label">
                Custom Package Details (Optional)
              </label>
              <input
                type="text"
                id="package_details"
                name="package_details"
                value={formData.package_details}
                onChange={handleInputChange}
                className="form-input"
                placeholder="E.g., Custom 10GB monthly bundle, Special router configuration"
              />
            </div>

            <div className="form-group">
              <label htmlFor="additional_notes" className="form-label">
                Additional Notes
              </label>
              <textarea
                id="additional_notes"
                name="additional_notes"
                value={formData.additional_notes}
                onChange={handleInputChange}
                className="form-textarea"
                rows="4"
                placeholder="Any special requirements, installation preferences, or additional information..."
              ></textarea>
            </div>

            {/* Order Summary */}
            {(formData.product_id || formData.package_details) && (
              <div className="order-summary">
                <h4>Order Summary</h4>
                <div className="summary-details">
                  <div className="summary-row">
                    <span>Product:</span>
                    <span>{getProductDetails()}</span>
                  </div>
                  <div className="summary-row">
                    <span>Total Price:</span>
                    <span className="total-price">TZS {getTotalPrice().toFixed(2)}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <div className="form-submit">
              <button 
                type="submit" 
                className="btn btn-primary btn-large"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <span className="spinner"></span>
                    Processing Order...
                  </>
                ) : (
                  'Place Order & Get Tracking'
                )}
              </button>
            </div>

            {/* Messages */}
            {message && (
              <div className={`message ${message.includes('✅') ? 'message-success' : 'message-error'}`}>
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