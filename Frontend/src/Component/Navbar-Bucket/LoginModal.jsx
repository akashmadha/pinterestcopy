import React, { useState } from 'react';
import { useCopilotReadable } from '@copilotkit/react-core'; 
import API_BASE_URL from '../../config';

function LoginModal({ isOpen, onClose, onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);


    // ✅ ADD THIS: Share login form state with AI
    useCopilotReadable({
        description: "Current login form state",
        value: `Login modal: ${isOpen ? 'open' : 'closed'}, Username: ${username || 'empty'}, Loading: ${loading}`
    });

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/api/login/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            console.log("📦 LoginModal - Response status:", response.status);
            
            // Check if response has content before parsing
            const text = await response.text();
            console.log("📦 LoginModal - Raw response:", text);
            
            let data;
            try {
                data = JSON.parse(text);
            } catch (e) {
                console.error("❌ LoginModal - Failed to parse JSON:", e);
                alert("Invalid response from server. Please try again.");
                return;
            }
            
            console.log("📦 LoginModal - Parsed response data:", data);
            
            if (response.ok && data.access) {
                localStorage.setItem("accessToken", data.access);
                if (data.refresh) {
                    localStorage.setItem("refreshToken", data.refresh);
                }
                if (onLogin) onLogin();
                onClose();
                // Reload to refresh the app state
                window.location.reload();
            } else {
                alert(data.error || "Login failed! Please check your credentials.");
            }
        } catch (error) {
            alert("Login failed! Please try again.");
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
        }}>
            <div style={{
                backgroundColor: 'white',
                padding: '40px',
                borderRadius: '16px',
                boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
                maxWidth: '400px',
                width: '90%',
                position: 'relative'
            }}>
                {/* Close button */}
                <button
                    onClick={onClose}
                    style={{
                        position: 'absolute',
                        top: '15px',
                        right: '15px',
                        background: 'none',
                        border: 'none',
                        fontSize: '24px',
                        cursor: 'pointer',
                        color: '#666'
                    }}
                >
                    ×
                </button>

                <div style={{ textAlign: 'center', marginBottom: '30px' }}>
                    <svg height="40" width="40" viewBox="0 0 24 24" aria-label="Pinterest logo" style={{ marginBottom: '10px' }}>
                        <path
                            fill="#e60023"
                            d="M0 12c0 5.123 3.211 9.497 7.73 11.218-.11-.937-.227-2.482.025-3.566.217-.932 1.401-5.938 1.401-5.938s-.357-.715-.357-1.774c0-1.66.962-2.9 2.161-2.9 1.02 0 1.512.765 1.512 1.682 0 1.025-.653 2.557-.99 3.978-.281 1.189.597 2.159 1.769 2.159 2.123 0 3.756-2.239 3.756-5.471 0-2.861-2.056-4.86-4.991-4.86-3.398 0-5.393 2.549-5.393 5.184 0 1.027.395 2.127.889 2.726a.36.36 0 0 1 .083.343c-.091.378-.293 1.189-.332 1.355-.053.218-.173.265-.4.159-1.492-.694-2.424-2.875-2.424-4.627 0-3.769 2.737-7.229 7.892-7.229 4.144 0 7.365 2.953 7.365 6.899 0 4.117-2.595 7.431-6.199 7.431-1.211 0-2.348-.63-2.738-1.373 0 0-.599 2.282-.744 2.84-.282 1.084-1.064 2.456-1.549 3.235C9.584 23.815 10.77 24 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0 0 5.373 0 12"
                        />
                    </svg>
                    <h2 style={{ fontSize: '28px', fontWeight: 'bold', color: '#333', margin: '0' }}>
                        Log in to Pinterest
                    </h2>
                </div>

                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>
                            Username
                        </label>
                        <input
                            type="text"
                            placeholder="Enter your username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            style={{
                                width: '100%',
                                padding: '16px',
                                border: '2px solid #ddd',
                                borderRadius: '16px',
                                fontSize: '16px',
                                outline: 'none',
                                boxSizing: 'border-box'
                            }}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>
                            Password
                        </label>
                        <input
                            type="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            style={{
                                width: '100%',
                                padding: '16px',
                                border: '2px solid #ddd',
                                borderRadius: '16px',
                                fontSize: '16px',
                                outline: 'none',
                                boxSizing: 'border-box'
                            }}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: '100%',
                            padding: '16px',
                            backgroundColor: loading ? '#ccc' : '#e60023',
                            color: 'white',
                            border: 'none',
                            borderRadius: '24px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            marginTop: '10px'
                        }}
                    >
                        {loading ? 'Logging in...' : 'Log in'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', margin: '20px 0', color: '#767676' }}>OR</div>
            <a href={`${API_BASE_URL}/accounts/google/login/?process=login`}>
                <button
                    type="button"
                    style={{
                        width: '100%',
                        padding: '16px',
                        backgroundColor: '#4285f4',
                        color: 'white',
                        border: 'none',
                        borderRadius: '24px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '10px'
                    }}
                >
                    <span>G</span> Continue with Google
                </button>
                </a>
            </div>
        </div>
    );
}

export default LoginModal;