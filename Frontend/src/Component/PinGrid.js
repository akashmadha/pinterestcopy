// src/components/PinGrid.js
import React from 'react';
import { useCopilotReadable } from '@copilotkit/react-core';

const PinGrid = ({ pins, currentUser }) => {
  // Make current pins available to AI
  useCopilotReadable({
    description: "Current pins displayed in the grid",
    value: pins.map(pin => `Pin: ${pin.title} - ${pin.description}`).join('\n')
  });

  // Make user info available to AI
  useCopilotReadable({
    description: "Current logged in user information",
    value: currentUser ? `User: ${currentUser.username}` : "No user logged in"
  });

  return (
    <div className="pin-grid">
      {/* Your existing pin grid rendering */}
      {pins.map(pin => (
        <div key={pin.id} className="pin-card">
          <img src={pin.imageUrl} alt={pin.title} />
          <h3>{pin.title}</h3>
          <p>{pin.description}</p>
        </div>
      ))}
    </div>
  );
};

export default PinGrid;