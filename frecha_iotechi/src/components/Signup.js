// Frontend Signup Component
import React, { useState } from 'react';
import axios from 'axios';

const SignupForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        password1: '',
        password2: ''
    });

    const handleSignup = async (e) => {
        e.preventDefault();
        
        if (formData.password1 !== formData.password2) {
            alert('Passwords do not match');
            return;
        }

        try {
            const response = await axios.post(
                'https://frecha-iotech.onrender.com/signup/',  // Your signup endpoint
                {
                    username: formData.username,
                    password1: formData.password1,
                    password2: formData.password2
                },
                { withCredentials: true }
            );
            
            console.log('Signup successful:', response.data);
            alert('Account created successfully! Please login.');
            window.location.href = '/login';
            
        } catch (error) {
            console.error('Signup failed:', error.response?.data);
            alert('Signup failed: ' + (error.response?.data?.error || 'Unknown error'));
        }
    };

    return (
        <div className="signup-form">
            <h2>Create Account</h2>
            <form onSubmit={handleSignup}>
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
                    value={formData.password1}
                    onChange={(e) => setFormData({...formData, password1: e.target.value})}
                    required
                />
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={formData.password2}
                    onChange={(e) => setFormData({...formData, password2: e.target.value})}
                    required
                />
                <button type="submit">Sign Up</button>
            </form>
            <p>Already have an account? <a href="/login">Login</a></p>
        </div>
    );
};