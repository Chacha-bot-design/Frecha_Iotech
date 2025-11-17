// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Header from './components/Header';
import ProductList from './components/ProductList';
import ShoppingCart from './components/ShoppingCart';
import CheckoutForm from './components/CheckoutForm';
import OrderSuccess from './components/OrderSuccess';
import OrderTracking from './components/OrderTracking';
import AuthModal from './components/AuthModal';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('products');
  const [cartItems, setCartItems] = useState([]);
  const [orderData, setOrderData] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);

  const addToCart = (product) => {
    setCartItems(prev => {
      const existingItem = prev.find(item => item.id === product.id && item.category === product.category);
      if (existingItem) {
        return prev.map(item =>
          item.id === product.id && item.category === product.category
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prev, { ...product, quantity: 1 }];
      }
    });
  };

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    
    setCartItems(prev =>
      prev.map(item =>
        item.id === itemId
          ? { ...item, quantity: newQuantity }
          : item
      )
    );
  };

  const removeFromCart = (itemId) => {
    setCartItems(prev => prev.filter(item => item.id !== itemId));
  };

  const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  const renderContent = () => {
    switch (currentView) {
      case 'products':
        return <ProductList onAddToCart={addToCart} />;
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
      default:
        return <ProductList onAddToCart={addToCart} />;
    }
  };

  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header 
            cartItemsCount={cartItems.reduce((sum, item) => sum + item.quantity, 0)}
            currentView={currentView}
            onNavigate={setCurrentView}
            onShowAuth={() => setShowAuthModal(true)}
          />
          
          <main>
            <Routes>
              <Route path="/" element={renderContent()} />
              <Route path="/track-order" element={<OrderTracking />} />
            </Routes>
          </main>

          <AuthModal
            isOpen={showAuthModal}
            onClose={() => setShowAuthModal(false)}
            onSuccess={() => setShowAuthModal(false)}
            showGuestOption={true}
          />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;