// OrderTrackingSignup.jsx
import React, { useState } from 'react';
import axios from 'axios';

const OrderTrackingSignup = () => {
    const [formData, setFormData] = useState({
        order_id: '',
        customer_email: '',
        customer_phone: ''
    });
    const [trackingInfo, setTrackingInfo] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSignup = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            const response = await axios.post(
                'https://frecha-iotech.onrender.com/api/tracking/signup/',
                formData
            );
            
            setTrackingInfo(response.data);
            alert('Order tracking activated successfully!');
            
        } catch (error) {
            alert(error.response?.data?.error || 'Failed to activate tracking');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="tracking-signup">
            <h2>Track Your Order</h2>
            <p>Enter your order details to track your shipment</p>
            
            {!trackingInfo ? (
                <form onSubmit={handleSignup} className="tracking-form">
                    <div className="form-group">
                        <label>Order ID:</label>
                        <input
                            type="text"
                            value={formData.order_id}
                            onChange={(e) => setFormData({...formData, order_id: e.target.value})}
                            placeholder="Enter your order ID"
                            required
                        />
                    </div>
                    
                    <div className="form-group">
                        <label>Email Address:</label>
                        <input
                            type="email"
                            value={formData.customer_email}
                            onChange={(e) => setFormData({...formData, customer_email: e.target.value})}
                            placeholder="Enter your email"
                            required
                        />
                    </div>
                    
                    <div className="form-group">
                        <label>Phone Number (optional):</label>
                        <input
                            type="tel"
                            value={formData.customer_phone}
                            onChange={(e) => setFormData({...formData, customer_phone: e.target.value})}
                            placeholder="Enter your phone number"
                        />
                    </div>
                    
                    <button type="submit" disabled={loading}>
                        {loading ? 'Activating Tracking...' : 'Track My Order'}
                    </button>
                </form>
            ) : (
                <div className="tracking-success">
                    <h3>✅ Tracking Activated!</h3>
                    <div className="tracking-details">
                        <p><strong>Tracking Number:</strong> {trackingInfo.tracking_number}</p>
                        <p><strong>Order Status:</strong> {trackingInfo.order_status}</p>
                        <p><strong>Customer:</strong> {trackingInfo.customer_name}</p>
                    </div>
                    <p>You will receive updates about your order status.</p>
                    <button onClick={() => setTrackingInfo(null)}>Track Another Order</button>
                </div>
            )}
        </div>
    );
};

export default OrderTrackingSignup;