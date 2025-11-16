// Frontend Login Component Example
import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const handleLogin = async (e) => {
        e.preventDefault();
        
        try {
            const response = await axios.post(
                'https://frecha-iotech.onrender.com/api/auth/login/',
                formData,
                { withCredentials: true }  // Important for sessions
            );
            
            console.log('Login successful:', response.data);
            // Save user data to context/state
            // Redirect to dashboard
            window.location.href = '/dashboard';
            
        } catch (error) {
            console.error('Login failed:', error.response?.data);
            alert('Login failed: ' + (error.response?.data?.error || 'Unknown error'));
        }
    };

    return (
        <div className="login-form">
            <h2>Login to Frecha IoTech</h2>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={formData.username}
                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    required
                />
                <button type="submit">Login</button>
            </form>
            <p>Don't have an account? <a href="/signup">Sign up</a></p>
        </div>
    );
};

export default LoginForm;