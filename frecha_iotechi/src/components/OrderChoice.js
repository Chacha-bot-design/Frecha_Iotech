
// components/OrderChoice.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const OrderChoice = ({ onGuestOrder, onSignUp }) => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            How would you like to proceed?
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Choose an option to continue with your order
          </p>
        </div>

        <div className="mt-8 space-y-6">
          {/* Guest Order Option */}
          <div 
            onClick={onGuestOrder}
            className="group relative flex flex-col items-center p-6 border-2 border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all duration-200"
          >
            <div className="text-4xl mb-4">🛒</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Continue as Guest
            </h3>
            <p className="text-sm text-gray-600 text-center">
              Quick checkout without creating an account. You can still track your order using your email and order number.
            </p>
            <ul className="mt-3 text-xs text-gray-500 space-y-1">
              <li>✓ Fast checkout</li>
              <li>✓ Order tracking via email</li>
              <li>✓ No password required</li>
            </ul>
          </div>

          {/* Sign Up Option */}
          <div 
            onClick={onSignUp}
            className="group relative flex flex-col items-center p-6 border-2 border-gray-300 rounded-lg cursor-pointer hover:border-green-500 hover:bg-green-50 transition-all duration-200"
          >
            <div className="text-4xl mb-4">👤</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Create Account
            </h3>
            <p className="text-sm text-gray-600 text-center">
              Sign up to track all your orders in one place and get faster checkout next time.
            </p>
            <ul className="mt-3 text-xs text-gray-500 space-y-1">
              <li>✓ Order history</li>
              <li>✓ Faster checkout</li>
              <li>✓ Personalized experience</li>
              <li>✓ Track multiple orders easily</li>
            </ul>
          </div>

          {/* Login Option */}
          <div className="text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <button
                onClick={() => navigate('/login')}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Sign in
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderChoice;