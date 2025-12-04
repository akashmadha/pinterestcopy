import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API_BASE_URL from "../../config";
import { useCopilotReadable } from '@copilotkit/react-core';

const Register = ({ setIsAuthenticated, onClose }) => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useCopilotReadable({
  description: "User registration form",
  value: `Username: ${username || 'empty'}, Email: ${email || 'empty'}, Message: ${message || 'none'}`
});

    const handleRegister = async (e) => {
        e.preventDefault();
        setMessage(""); // Clear previous messages

        console.log("🔄 Attempting registration...");

        try {
            const response = await fetch(`${API_BASE_URL}/api/register/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();
            console.log("📦 Registration response:", data);

            if (response.ok) {
                setMessage("Registration successful! ✅");
                
                // ✅ If the backend returns tokens on registration, save them
                if (data.access && data.refresh) {
                    localStorage.setItem("accessToken", data.access);
                    localStorage.setItem("refreshToken", data.refresh);
                    setIsAuthenticated(true);
                    console.log("💾 Tokens saved after registration");
                }
                
                setTimeout(() => {
                    if (onClose) onClose(); // Close popup if exists
                    navigate("/login"); // Redirect to login page
                }, 1500);
            } else {
                // ✅ Show specific error messages from backend
                const errorMsg = data.error || data.username?.[0] || data.email?.[0] || data.password?.[0] || "Registration failed. Try again.";
                setMessage(errorMsg);
                console.error("❌ Registration failed:", data);
            }
        } catch (error) {
            console.error("❌ Network error:", error);
            setMessage("Network error. Please try again.");
        }
    };

    return (
        <div style={{ 
            display: 'flex', 
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: 'calc(100vh - 80px)',
            padding: '20px'
        }}>

            {/* Register Form */}
            <div style={{ 
                maxWidth: '400px', 
                width: '100%',
                backgroundColor: 'white', 
                padding: '40px', 
                borderRadius: '16px', 
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                textAlign: 'center'
            }}>
                <h2 style={{ fontSize: '32px', fontWeight: 'bold', color: '#333', marginBottom: '10px' }}>
                    Welcome to Pinterest
                </h2>
                <p style={{ color: '#767676', marginBottom: '30px' }}>Find new ideas to try</p>
                
                {message && (
                    <p style={{ 
                        padding: '10px', 
                        backgroundColor: message.includes('successful') ? '#d4edda' : '#f8d7da',
                        color: message.includes('successful') ? '#155724' : '#721c24',
                        border: `1px solid ${message.includes('successful') ? '#c3e6cb' : '#f5c6cb'}`,
                        borderRadius: '4px',
                        marginBottom: '15px',
                        fontSize: '14px'
                    }}>
                        {message}
                    </p>
                )}
                
                <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    <div style={{ textAlign: 'left' }}>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>
                            User Name
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
                                boxSizing: 'border-box',
                                transition: 'border-color 0.3s'
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#e60023'}
                            onBlur={(e) => e.target.style.borderColor = '#ddd'}
                        />
                    </div>

                    <div style={{ textAlign: 'left' }}>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>
                            Email Address
                        </label>
                        <input
                            type="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            style={{ 
                                width: '100%', 
                                padding: '16px', 
                                border: '2px solid #ddd', 
                                borderRadius: '16px', 
                                fontSize: '16px',
                                outline: 'none',
                                boxSizing: 'border-box',
                                transition: 'border-color 0.3s'
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#e60023'}
                            onBlur={(e) => e.target.style.borderColor = '#ddd'}
                        />
                    </div>

                    <div style={{ textAlign: 'left' }}>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>
                            New Password
                        </label>
                        <input
                            type="password"
                            placeholder="Create a strong password"
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
                                boxSizing: 'border-box',
                                transition: 'border-color 0.3s'
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#e60023'}
                            onBlur={(e) => e.target.style.borderColor = '#ddd'}
                        />
                    </div>

                    <button 
                        type="submit"
                        style={{ 
                            width: '100%',
                            padding: '16px', 
                            backgroundColor: '#e60023', 
                            color: 'white', 
                            border: 'none', 
                            borderRadius: '24px', 
                            fontSize: '16px', 
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            marginTop: '10px',
                            transition: 'background-color 0.3s'
                        }}
                        onMouseOver={(e) => e.target.style.backgroundColor = '#ad081b'}
                        onMouseOut={(e) => e.target.style.backgroundColor = '#e60023'}
                    >
                        Continue
                    </button>
                </form>
                
                <p style={{ marginTop: '20px', color: '#767676' }}>
                    Already have an account? <a href="/login" style={{ color: '#e60023', textDecoration: 'none', fontWeight: 'bold' }}>Log in here</a>
                </p>

                {/* Debug Info */}
                <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '8px', fontSize: '12px', color: '#666' }}>
                    <strong>Debug Info:</strong>
                    <br />
                    Tokens in localStorage: {localStorage.getItem("accessToken") ? "Yes ✅" : "No ❌"}
                </div>
            </div>
        </div>
    );
};

export default Register;