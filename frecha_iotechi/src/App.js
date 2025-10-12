// App.js - Public frontend with optional login
import React, { useState, useEffect } from 'react';
import { 
  getPublicProviders, 
  getPublicBundles, 
  getPublicRouters,
  getProtectedProviders,
  login,
  logout,
  getCurrentUser
} from './api';

function App() {
  const [user, setUser] = useState(null);
  const [publicData, setPublicData] = useState({
    providers: [],
    bundles: [], 
    routers: []
  });
  const [protectedData, setProtectedData] = useState({
    providers: [],
    bundles: [],
    routers: []
  });
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });

  // Load public data on component mount
  useEffect(() => {
    loadPublicData();
    checkAuth();
  }, []);

  const loadPublicData = async () => {
    try {
      const [providers, bundles, routers] = await Promise.all([
        getPublicProviders(),
        getPublicBundles(), 
        getPublicRouters()
      ]);
      
      setPublicData({
        providers: providers.data.data,
        bundles: bundles.data.data,
        routers: routers.data.data
      });
    } catch (error) {
      console.error('Error loading public data:', error);
    }
  };

  const checkAuth = async () => {
    try {
      const userData = await getCurrentUser();
      setUser(userData.user);
      loadProtectedData();
    } catch (error) {
      setUser(null);
    }
  };

  const loadProtectedData = async () => {
    if (!user) return;
    
    try {
      const [providers, bundles, routers] = await Promise.all([
        getProtectedProviders(),
        getProtectedBundles(),
        getProtectedRouters()
      ]);
      
      setProtectedData({
        providers: providers.data.data,
        bundles: bundles.data.data,
        routers: routers.data.data
      });
    } catch (error) {
      console.error('Error loading protected data:', error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await login(loginForm.username, loginForm.password);
      setUser(response.user);
      loadProtectedData();
    } catch (error) {
      alert('Login failed');
    }
  };

  const handleLogout = async () => {
    await logout();
    setUser(null);
    setProtectedData({ providers: [], bundles: [], routers: [] });
  };

  return (
    <div className="App">
      <header>
        <h1>My Website</h1>
        {user ? (
          <div>
            <span>Welcome, {user.username}!</span>
            <button onClick={handleLogout}>Logout</button>
          </div>
        ) : (
          <form onSubmit={handleLogin} style={{display: 'inline'}}>
            <input
              type="text"
              placeholder="Username"
              value={loginForm.username}
              onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
            />
            <input
              type="password"
              placeholder="Password"
              value={loginForm.password}
              onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
            />
            <button type="submit">Login</button>
          </form>
        )}
      </header>

      {/* PUBLIC CONTENT - Anyone can see */}
      <section>
        <h2>Our Services (Public)</h2>
        
        <div>
          <h3>Providers</h3>
          {publicData.providers.map(item => (
            <div key={item.id}>{item.name} - {item.type}</div>
          ))}
        </div>

        <div>
          <h3>Bundles</h3>
          {publicData.bundles.map(item => (
            <div key={item.id}>{item.name} - ${item.price}</div>
          ))}
        </div>

        <div>
          <h3>Routers</h3>
          {publicData.routers.map(item => (
            <div key={item.id}>{item.name} - {item.type}</div>
          ))}
        </div>
      </section>

      {/* PROTECTED CONTENT - Only logged-in users can see */}
      {user && (
        <section style={{background: '#f5f5f5', padding: '20px', marginTop: '20px'}}>
          <h2>Member Area (Protected)</h2>
          <p>This content is only visible to logged-in users</p>
          
          <div>
            <h3>Full Provider Details</h3>
            {protectedData.providers.map(item => (
              <div key={item.id}>
                {item.name} - {item.email} - {item.phone}
              </div>
            ))}
          </div>

          <div>
            <h3>Full Bundle Details</h3>
            {protectedData.bundles.map(item => (
              <div key={item.id}>
                {item.name} - ${item.price} - {item.description}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default App;