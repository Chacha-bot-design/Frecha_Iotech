// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Header from './components/Header';
import ProductList from './components/ProductList';
import ShoppingCart from './components/ShoppingCart';
import CheckoutForm from './components/CheckoutForm';
import OrderSuccess from './components/OrderSuccess';
import OrderTracking from './components/OrderTracking';
import UserProfile from './components/UserProfile';
import AuthModal from './components/AuthModal';

function AppContent() {
  const [currentView, setCurrentView] = useState('products');
  const [cartItems, setCartItems] = useState([]);
  const [orderData, setOrderData] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const { isAuthenticated } = useAuth();

  // ... your existing product and cart logic ...

  const renderContent = () => {
    switch (currentView) {
      case 'products':
        return (
          <ProductList 
            products={products} 
            onAddToCart={addToCart} 
          />
        );
      case 'cart':
        return (
          <ShoppingCart
            cartItems={cartItems}
            onUpdateQuantity={updateQuantity}
            onRemoveItem={removeFromCart}
            onProceedToCheckout={() => setCurrentView('checkout')}
          />
        );
      case 'checkout':
        return (
          <CheckoutForm
            cartItems={cartItems}
            total={total}
            onOrderSuccess={(data) => {
              setOrderData(data);
              setCurrentView('success');
              setCartItems([]);
            }}
            onBackToCart={() => setCurrentView('cart')}
          />
        );
      case 'success':
        return (
          <OrderSuccess
            orderData={orderData}
            onContinueShopping={() => {
              setCurrentView('products');
              setOrderData(null);
            }}
          />
        );
      case 'tracking':
        return <OrderTracking />;
      case 'profile':
        return isAuthenticated ? <UserProfile /> : <Navigate to="/" />;
      default:
        return <ProductList products={products} onAddToCart={addToCart} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        cartItemsCount={cartItems.length}
        currentView={currentView}
        onNavigate={setCurrentView}
        onShowAuth={() => setShowAuthModal(true)}
      />
      
      <main className="container mx-auto px-4 py-8">
        {renderContent()}
      </main>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onSuccess={() => setShowAuthModal(false)}
        showGuestOption={true}
      />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<AppContent />} />
          <Route path="/track-order" element={<OrderTracking />} />
          <Route path="/profile" element={<UserProfile />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;