// App.js
import React, { useState, useEffect } from 'react';
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

// Sample products data
const sampleProducts = [
  {
    id: 1,
    name: "Wireless Bluetooth Headphones",
    price: 79.99,
    description: "High-quality wireless headphones with noise cancellation",
    image: "/images/headphones.jpg",
    category: "Electronics",
    inStock: true
  },
  {
    id: 2,
    name: "Smart Fitness Watch",
    price: 199.99,
    description: "Track your fitness goals with this advanced smartwatch",
    image: "/images/smartwatch.jpg",
    category: "Electronics",
    inStock: true
  },
  {
    id: 3,
    name: "Organic Cotton T-Shirt",
    price: 29.99,
    description: "Comfortable and eco-friendly cotton t-shirt",
    image: "/images/tshirt.jpg",
    category: "Clothing",
    inStock: true
  },
  {
    id: 4,
    name: "Stainless Steel Water Bottle",
    price: 24.99,
    description: "Keep your drinks hot or cold for hours",
    image: "/images/water-bottle.jpg",
    category: "Accessories",
    inStock: true
  }
];

function AppContent() {
  const [currentView, setCurrentView] = useState('products');
  const [cartItems, setCartItems] = useState([]);
  const [orderData, setOrderData] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const { isAuthenticated } = useAuth();

  // Load cart from localStorage on component mount
  useEffect(() => {
    const savedCart = localStorage.getItem('cartItems');
    if (savedCart) {
      setCartItems(JSON.parse(savedCart));
    }
  }, []);

  // Save cart to localStorage whenever cartItems change
  useEffect(() => {
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
  }, [cartItems]);

  // Product and cart management functions
  const addToCart = (product) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === product.id);
      
      if (existingItem) {
        return prevItems.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prevItems, { ...product, quantity: 1 }];
      }
    });
  };

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity < 1) {
      removeFromCart(productId);
      return;
    }

    setCartItems(prevItems =>
      prevItems.map(item =>
        item.id === productId
          ? { ...item, quantity: newQuantity }
          : item
      )
    );
  };

  const removeFromCart = (productId) => {
    setCartItems(prevItems => prevItems.filter(item => item.id !== productId));
  };

  const clearCart = () => {
    setCartItems([]);
  };

  // Calculate total price
  const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  const renderContent = () => {
    switch (currentView) {
      case 'products':
        return (
          <ProductList 
            products={sampleProducts} 
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
            onContinueShopping={() => setCurrentView('products')}
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
            onShowAuth={() => setShowAuthModal(true)}
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
            onTrackOrder={() => setCurrentView('tracking')}
          />
        );
      case 'tracking':
        return <OrderTracking />;
      case 'profile':
        return isAuthenticated ? <UserProfile /> : <Navigate to="/" />;
      default:
        return <ProductList products={sampleProducts} onAddToCart={addToCart} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        cartItemsCount={cartItems.reduce((count, item) => count + item.quantity, 0)}
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
          <Route path="/products" element={<AppContent />} />
          <Route path="/cart" element={<AppContent />} />
          <Route path="/checkout" element={<AppContent />} />
          <Route path="/order-success" element={<AppContent />} />
          <Route path="/track-order" element={<OrderTracking />} />
          <Route path="/profile" element={<UserProfile />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;