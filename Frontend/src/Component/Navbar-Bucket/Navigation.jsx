import React, { useState } from 'react';
import LoginModal from './LoginModal';
import SignupModal from './SignupModal';
import { useCopilotReadable } from '@copilotkit/react-core';

import './Navigation.css';

function Navigation({ setIsAuthenticated }) {
    const [isLoginOpen, setIsLoginOpen] = useState(false);
    const [isSignupOpen, setIsSignupOpen] = useState(false);
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    
     useCopilotReadable({
        description: "Current navigation and authentication state",
        value: `Login modal: ${isLoginOpen ? 'open' : 'closed'}, Signup modal: ${isSignupOpen ? 'open' : 'closed'}, Menu: ${isMenuOpen ? 'open' : 'closed'}, User: not authenticated`
    });


    const handleLogin = () => {
        setIsAuthenticated(true);
    };

    const handleSignup = () => {
        // After successful signup, you might want to open login modal
        setIsSignupOpen(false);
        setIsLoginOpen(true);
    };

    return (    
        <>
            {/* Navigation Bar */}
            <nav style={{
                width: '100%',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '2vh 6vw',
                backgroundColor: 'white',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                zIndex: 999
            }}>
                <div

  className="menu-wrapper"
>
  <button
    className="nav-hamburger"
    aria-label="Toggle menu"
    onClick={() => setIsMenuOpen(!isMenuOpen)}
  >
    <span className="bar" />
    <span className="bar" />
    <span className="bar" />
  </button>
</div>
                <div className="nav-brand">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><svg height="32" width="32" viewBox="0 0 24 24" aria-label="Pinterest logo">
                        <path
                            fill="#e60023"
                            d="M0 12c0 5.123 3.211 9.497 7.73 11.218-.11-.937-.227-2.482.025-3.566.217-.932 1.401-5.938 1.401-5.938s-.357-.715-.357-1.774c0-1.66.962-2.9 2.161-2.9 1.02 0 1.512.765 1.512 1.682 0 1.025-.653 2.557-.99 3.978-.281 1.189.597 2.159 1.769 2.159 2.123 0 3.756-2.239 3.756-5.471 0-2.861-2.056-4.86-4.991-4.86-3.398 0-5.393 2.549-5.393 5.184 0 1.027.395 2.127.889 2.726a.36.36 0 0 1 .083.343c-.091.378-.293 1.189-.332 1.355-.053.218-.173.265-.4.159-1.492-.694-2.424-2.875-2.424-4.627 0-3.769 2.737-7.229 7.892-7.229 4.144 0 7.365 2.953 7.365 6.899 0 4.117-2.595 7.431-6.199 7.431-1.211 0-2.348-.63-2.738-1.373 0 0-.599 2.282-.744 2.84-.282 1.084-1.064 2.456-1.549 3.235C9.584 23.815 10.77 24 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0 0 5.373 0 12"
                        />
                    </svg>
                    <span style={{ fontSize: '22px', fontWeight: 'bold', color: '#333' }}>Pinterest</span></div>
                    <div className='explore'>
                        <button>Explore</button>
                    </div>
                    

                </div>

                <div className={`nav-actions ${isMenuOpen ? 'open' : ''}`} style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <button style={{ 
                        background: 'none', 
                        border: 'none', 
                        color: '#333', 
                        cursor: 'pointer',
                        fontSize: '16px',
                        fontWeight: '600',
                        padding: '8px 12px',
                        borderRadius: '8px',
                        transition: 'background-color 0.2s'
                    }}>
                        Explore
                    </button>
                    <button style={{ 
                        background: 'none', 
                        border: 'none', 
                        color: '#333', 
                        cursor: 'pointer',
                        fontSize: '16px',
                        fontWeight: '600',
                        padding: '8px 12px',
                        borderRadius: '8px',
                        transition: 'background-color 0.2s'
                    }}>
                        About
                    </button>
                    <button style={{ 
                        background: 'none', 
                        border: 'none', 
                        color: '#333', 
                        cursor: 'pointer',
                        fontSize: '16px',
                        fontWeight: '600',
                        padding: '8px 12px',
                        borderRadius: '8px',
                        transition: 'background-color 0.2s'
                    }}>
                        Business
                    </button>
                    <button style={{ 
                        background: 'none', 
                        border: 'none', 
                        color: '#333', 
                        cursor: 'pointer',
                        fontSize: '16px',
                        fontWeight: '600',
                        padding: '8px 12px',
                        borderRadius: '8px',
                        transition: 'background-color 0.2s'
                    }}>
                        Press
                    </button>
                    
                    <button 
                        onClick={() => setIsLoginOpen(true)}
                        style={{ 
                            backgroundColor: '#e60023', 
                            color: 'white', 
                            padding: '12px 20px', 
                            borderRadius: '24px', 
                            border: 'none',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            transition: 'background-color 0.2s'
                        }}
                    >
                        Log in
                    </button>
                    
                    <button 
                        onClick={() => setIsSignupOpen(true)}
                        style={{ 
                            backgroundColor: '#efefef', 
                            color: '#333', 
                            padding: '12px 20px', 
                            borderRadius: '24px', 
                            border: 'none',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            transition: 'background-color 0.2s'
                        }}
                    >
                        Sign up
                    </button>
                </div>
            </nav>

            {/* Modals */}
            <LoginModal 
                isOpen={isLoginOpen} 
                onClose={() => setIsLoginOpen(false)} 
                onLogin={handleLogin}
            />
            <SignupModal 
                isOpen={isSignupOpen} 
                onClose={() => setIsSignupOpen(false)} 
                onSignup={handleSignup}
            />
        </>
    );
}

export default Navigation;