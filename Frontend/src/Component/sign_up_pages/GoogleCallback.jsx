import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const GoogleCallback = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();

  useEffect(() => {
    // Extract tokens from URL hash
    const hash = window.location.hash.substring(1); // Remove the '#'
    const params = new URLSearchParams(hash);
    
    const accessToken = params.get('access');
    const refreshToken = params.get('refresh');
    const username = params.get('username');
    const email = params.get('email');
    const error = params.get('error');

    if (error) {
      console.error('Google OAuth error:', error);
      alert(`Google login failed: ${error}`);
      navigate('/login');
      return;
    }

    if (accessToken && refreshToken) {
      // Store tokens in localStorage
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', refreshToken);
      
      // Store user profile if available
      if (username || email) {
        localStorage.setItem(
          'userProfile',
          JSON.stringify({
            username: username || '',
            email: email || '',
          })
        );
      }

      console.log('✅ Google OAuth tokens stored successfully');
      
      // Update authentication state
      if (setIsAuthenticated) {
        setIsAuthenticated(true);
      }

      // Redirect to home page
      navigate('/home');
    } else {
      console.error('❌ No tokens found in callback URL');
      alert('Google login failed: No tokens received');
      navigate('/login');
    }
  }, [navigate, setIsAuthenticated]);

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      backgroundColor: '#f7f7f7'
    }}>
      <div style={{
        textAlign: 'center',
        padding: '40px',
        backgroundColor: 'white',
        borderRadius: '16px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)'
      }}>
        <h2>Completing Google login...</h2>
        <p>Please wait while we sign you in.</p>
      </div>
    </div>
  );
};

export default GoogleCallback;

