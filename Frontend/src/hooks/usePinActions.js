// src/hooks/usePinActions.js
import { useCopilotAction } from '@copilotkit/react-core';

export const usePinActions = () => {
  // Action to search pins
  useCopilotAction({
    name: "searchPins",
    description: "Search for pins by keywords",
    parameters: [
      {
        name: "query",
        type: "string",
        description: "Search keywords for pins",
        required: true
      }
    ],
    handler: async ({ query }) => {
      alert(`Searching for pins: ${query}`);
      console.log('Search query:', query);
    },
  });

  // Navigation actions
  useCopilotAction({
    name: "navigateToProfile",
    description: "Navigate to user profile page",
    parameters: [],
    handler: async () => {
      window.location.href = "/UserProfile";
    },
  });

  useCopilotAction({
    name: "navigateToExplore", 
    description: "Navigate to explore page",
    parameters: [],
    handler: async () => {
      window.location.href = "/explore";
    },
  });

  useCopilotAction({
    name: "navigateToHome",
    description: "Navigate to home page", 
    parameters: [],
    handler: async () => {
      window.location.href = "/home";
    },
  });

  useCopilotAction({
    name: "logoutUser",
    description: "Log out the current user",
    parameters: [],
    handler: async () => {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken"); 
      window.location.href = "/login";
    },
  });

  // Fallback actions for AI's generic function names
  useCopilotAction({
    name: "set_active_sidebar_tab",
    description: "Set active sidebar tab",
    parameters: [
      {
        name: "tab",
        type: "string",
        description: "Tab name: home, explore, profile, etc.",
        required: true
      }
    ],
    handler: async ({ tab }) => {
      if (tab === "profile") {
        window.location.href = "/UserProfile";
      } else if (tab === "explore") {
        window.location.href = "/explore";
      } else if (tab === "home") {
        window.location.href = "/home";
      }
    },
  });

  useCopilotAction({
    name: "logout_user", 
    description: "Log out user",
    parameters: [],
    handler: async () => {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      window.location.href = "/login";
    },
  });

  // Action to create a board
  useCopilotAction({
    name: "createBoard",
    description: "Create a new board for pins",
    parameters: [
      {
        name: "boardName",
        type: "string",
        description: "Name of the new board",
        required: true
      }
    ],
    handler: async ({ boardName }) => {
      alert(`Creating board: ${boardName}`);
      console.log('Creating board:', boardName);
    },
  });

  // Action to suggest categories
  useCopilotAction({
    name: "suggestCategories",
    description: "Suggest popular pin categories",
    parameters: [],
    handler: async () => {
      const categories = [
        "Home Decor", "Recipes", "Travel", 
        "Fashion", "DIY Projects", "Fitness"
      ];
      alert(`Popular categories: ${categories.join(', ')}`);
    },
  });
}; // ✅ All actions are inside the function now