// OrderTrackingLookup.jsx
import React, { useState } from 'react';
import axios from 'axios';

const OrderTrackingLookup = () => {
    const [trackingNumber, setTrackingNumber] = useState('');
    const [orderDetails, setOrderDetails] = useState(null);
    const [loading, setLoading] = useState(false);

    const trackOrder = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            const response = await axios.get(
                `https://frecha-iotech.onrender.com/api/tracking/${trackingNumber}/`
            );
            
            setOrderDetails(response.data);
        } catch (error) {
            alert(error.response?.data?.error || 'Order not found');
            setOrderDetails(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="tracking-lookup">
            <h2>Check Order Status</h2>
            
            <form onSubmit={trackOrder} className="lookup-form">
                <input
                    type="text"
                    value={trackingNumber}
                    onChange={(e) => setTrackingNumber(e.target.value)}
                    placeholder="Enter your tracking number"
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Searching...' : 'Track Order'}
                </button>
            </form>
            
            {orderDetails && (
                <div className="order-status">
                    <h3>Order Status: {orderDetails.status_display}</h3>
                    <div className="order-info">
                        <p><strong>Customer:</strong> {orderDetails.customer_name}</p>
                        <p><strong>Product:</strong> {orderDetails.product_details}</p>
                        <p><strong>Order Date:</strong> {new Date(orderDetails.order_date).toLocaleDateString()}</p>
                    </div>
                    
                    <div className="status-timeline">
                        <h4>Status Updates:</h4>
                        {orderDetails.status_updates?.map((update, index) => (
                            <div key={index} className="status-update">
                                <strong>{update.status}</strong> - {new Date(update.timestamp).toLocaleString()}
                                {update.notes && <p>Note: {update.notes}</p>}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};