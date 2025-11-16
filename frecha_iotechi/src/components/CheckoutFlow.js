// components/CheckoutFlow.js
import React, { useState } from 'react';
import OrderChoice from './OrderChoice';
import GuestCheckout from './GuestCheckout';
import SignUpForm from './SignUpForm';
import OrderSuccess from './OrderSuccess';

const CheckoutFlow = ({ cartItems, total, onBackToCart }) => {
  const [currentStep, setCurrentStep] = useState('choice'); // choice, guest, signup, success
  const [orderData, setOrderData] = useState(null);

  const handleGuestOrder = () => {
    setCurrentStep('guest');
  };

  const handleSignUp = () => {
    setCurrentStep('signup');
  };

  const handleOrderSuccess = (data) => {
    setOrderData(data);
    setCurrentStep('success');
  };

  const handleBackToChoice = () => {
    setCurrentStep('choice');
  };

  const renderStep = () => {
    switch (currentStep) {
      case 'choice':
        return (
          <OrderChoice 
            onGuestOrder={handleGuestOrder}
            onSignUp={handleSignUp}
          />
        );
      
      case 'guest':
        return (
          <GuestCheckout
            cartItems={cartItems}
            total={total}
            onOrderSuccess={handleOrderSuccess}
            onBack={handleBackToChoice}
          />
        );
      
      case 'signup':
        return (
          <SignUpForm
            cartItems={cartItems}
            total={total}
            onOrderSuccess={handleOrderSuccess}
            onBack={handleBackToChoice}
          />
        );
      
      case 'success':
        return (
          <OrderSuccess
            orderData={orderData}
            onContinueShopping={() => window.location.href = '/'}
          />
        );
      
      default:
        return null;
    }
  };

  return (
    <div>
      {currentStep !== 'choice' && currentStep !== 'success' && (
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <button
              onClick={handleBackToChoice}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              ← Back to Options
            </button>
          </div>
        </div>
      )}
      {renderStep()}
    </div>
  );
};

export default CheckoutFlow;