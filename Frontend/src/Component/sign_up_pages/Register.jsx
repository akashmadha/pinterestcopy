import { useState } from "react";

const Register = ({ setIsAuthenticated }) => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const handleRegister = async (e) => {
        e.preventDefault();

        const response = await fetch("https://pinterestclone-backend.onrender.com/api/register/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            setMessage("Registration successful! Redirecting...");
            setTimeout(() => {
                window.location.href = "/login"; // Redirect to login page
            }, 1500);
        } else {
            setMessage(data.error || "Registration failed. Try again.");
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
                        marginBottom: '15px'
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
                                boxSizing: 'border-box'
                            }}
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
                                boxSizing: 'border-box'
                            }}
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
                                boxSizing: 'border-box'
                            }}
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
                            marginTop: '10px'
                        }}
                    >
                        Continue
                    </button>
                </form>
                
                <p style={{ marginTop: '20px', color: '#767676' }}>
                    Already have an account? <a href="/login" style={{ color: '#e60023', textDecoration: 'none', fontWeight: 'bold' }}>Log in here</a>
                </p>
            </div>
        </div>
    );
};

export default Register;
