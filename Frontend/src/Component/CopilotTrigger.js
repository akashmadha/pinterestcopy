// Component/CopilotTrigger.js
import React from 'react';
import { useCopilotContext } from '@copilotkit/react-core';

const CopilotTrigger = () => {
  const { setChatOpen } = useCopilotContext(); // ✅ Use setChatOpen instead of setContext
  
  return (
    <button 
      onClick={() => setChatOpen(true)} // ✅ Use setChatOpen to open the chat
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        backgroundColor: '#e60023',
        color: 'white',
        border: 'none',
        borderRadius: '50%',
        width: '60px',
        height: '60px',
        fontSize: '24px',
        cursor: 'pointer',
        boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      AI
    </button>
  );
};

export default CopilotTrigger;