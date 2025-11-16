// src/components/ProductList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProductList = ({ onAddToCart }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('electronics');

  useEffect(() => {
    fetchProducts();
  }, [activeTab]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      let response;
      
      if (activeTab === 'electronics') {
        response = await axios.get('/store/api/electronics/');
      } else if (activeTab === 'routers') {
        response = await axios.get('/store/api/public-routers/');
      } else if (activeTab === 'bundles') {
        response = await axios.get('/store/api/public-bundles/');
      }
      
      setProducts(response.data || []);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (product) => {
    const cartItem = {
      id: product.id || Math.random(),
      name: product.name,
      price: parseFloat(product.price),
      quantity: 1,
      image: product.image,
      category: activeTab
    };
    onAddToCart(cartItem);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500 text-lg">{error}</p>
        <button 
          onClick={fetchProducts}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-8">
        <button
          className={`py-2 px-4 font-medium ${
            activeTab === 'electronics'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('electronics')}
        >
          Electronics
        </button>
        <button
          className={`py-2 px-4 font-medium ${
            activeTab === 'routers'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('routers')}
        >
          Routers
        </button>
        <button
          className={`py-2 px-4 font-medium ${
            activeTab === 'bundles'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('bundles')}
        >
          Data Bundles
        </button>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-500 text-lg">No products available</p>
          </div>
        ) : (
          products.map((product) => (
            <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              {/* Product Image */}
              <div className="h-48 bg-gray-200 flex items-center justify-center">
                {product.image ? (
                  <img 
                    src={product.image} 
                    alt={product.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="text-gray-400">
                    <i className="bi bi-image text-4xl"></i>
                    <p className="mt-2">No Image</p>
                  </div>
                )}
              </div>

              {/* Product Info */}
              <div className="p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  {product.name}
                </h3>
                
                {product.description && (
                  <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                    {product.description}
                  </p>
                )}

                {product.specifications && (
                  <p className="text-gray-500 text-xs mb-3">
                    {product.specifications.length > 100 
                      ? `${product.specifications.substring(0, 100)}...`
                      : product.specifications
                    }
                  </p>
                )}

                {/* Bundle specific info */}
                {product.data_volume && (
                  <div className="mb-2">
                    <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {product.data_volume}
                    </span>
                    {product.validity_days && (
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded ml-1">
                        {product.validity_days} days
                      </span>
                    )}
                  </div>
                )}

                {/* Provider info for bundles */}
                {product.provider_name && (
                  <p className="text-gray-500 text-sm mb-2">
                    Provider: {product.provider_name}
                  </p>
                )}

                {/* Price and Action */}
                <div className="flex justify-between items-center mt-4">
                  <span className="text-xl font-bold text-green-600">
                    TZS {parseFloat(product.price).toLocaleString()}
                  </span>
                  <button
                    onClick={() => handleAddToCart(product)}
                    className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2"
                  >
                    <i className="bi bi-cart-plus"></i>
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ProductList;