import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { usePinActions } from './hooks/usePinActions';
import { CopilotKit } from '@copilotkit/react-core';
import { CopilotPopup } from '@copilotkit/react-ui'; // ✅ Changed from CopilotSidebar to CopilotPopup
import "@copilotkit/react-ui/styles.css";

// 🧱 Authentication components
import Register from "./Component/sign_up_pages/Register";
import Login from "./Component/sign_up_pages/Login";
import Logout from "./Component/sign_up_pages/Logout";
import GoogleCallback from "./Component/sign_up_pages/GoogleCallback";

// 🧭 Layout + UI components
import Navbar from "./Component/Navbar-Bucket/Navbar";
import Sidebar from "./Component/Navbar-Bucket/Sidebar";
import Navigation from "./Component/Navbar-Bucket/Navigation";
import PinterestAPI from "./Component/PinterestAPI";

// 🧩 Sidebar-linked routes
import Create from './Component/sidebar_buttons/Create';
import Explore from './Component/sidebar_buttons/Explore';
import Messages from './Component/sidebar_buttons/Messages';
import Home from './Component/Home';
import Notifications from './Component/sidebar_buttons/Notifications';
import UserProfile from "./Component/Navbar-Bucket/UserProfile";

// Create a component that uses Copilot hooks
const AuthenticatedApp = ({ 
  setIsAuthenticated, 
  searchQuery, 
  setSearchQuery, 
  selectedTags, 
  setSelectedTags, 
  hideSidebarNavbar 
}) => {
  return (
    <>
      <Sidebar />

      {!hideSidebarNavbar && (
        <div className="pin_nav_continer">
          <Navbar
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            selectedTags={selectedTags}
            setSelectedTags={setSelectedTags}
          />
          <PinterestAPI
            searchQuery={searchQuery}
            selectedTags={selectedTags}
          />
          
        </div>
      )}

      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/explore" element={<Explore />} />
        <Route path="/create" element={<Create />} />
        <Route path="/messages" element={<Messages />} />
        <Route path="/register" element={<Register />} />
        <Route path="/notifications" element={<Notifications />} />
         
        <Route
          path="/logout"
          element={<Logout setIsAuthenticated={setIsAuthenticated} />}
        />
        <Route path="*" element={<Navigate to="/home" />} />
        <Route path="/UserProfile" element={<UserProfile />} />
      </Routes>
    </>
  );
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);
  const location = useLocation();

  const pagesWithoutSidebarNavbar = [
    "/explore", "/create", "/messages", "/notifications", 
    "/login", "/register", "/UserProfile",
  ];

  const hideSidebarNavbar = pagesWithoutSidebarNavbar.includes(location.pathname);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    setIsAuthenticated(!!token);
  }, [location.pathname]);

  return (
    <CopilotKit publicApiKey="ck_pub_a65a45f717267747a71954acd730ddf5">
      {!isAuthenticated ? (
        <>
          <Navigation setIsAuthenticated={setIsAuthenticated} />
          <div
            style={{
              paddingTop: "80px",
              minHeight: "100vh",
              backgroundColor: "#f7f7f7",
            }}
          >
            <Routes>
              <Route
                path="/login"
                element={<Login setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/register"
                element={<Register setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/google-callback"
                element={<GoogleCallback setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
          </div>
        </>
      ) : (
        <AuthenticatedApp 
          setIsAuthenticated={setIsAuthenticated}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          selectedTags={selectedTags}
          setSelectedTags={setSelectedTags}
          hideSidebarNavbar={hideSidebarNavbar}
        />
      )}
      
      {/* ✅ SIMPLE - CopilotKit will automatically add a chat button */}
      <CopilotPopup 
        instructions={`
You are a Pinterest assistant. Use these EXACT action names:

NAVIGATION:
- "go to profile" → use navigateToProfile
- "open explore" → use navigateToExplore  
- "take me home" → use navigateToHome
- "logout" → use logoutUser

SEARCH:
- "search for [query]" → use searchPins

BOARDS:
- "create board [name]" → use createBoard

Always use the exact action names above. Don't make up functions like set_active_sidebar_tab() or logout_user().
`}
        defaultOpen={false}
        
      />
    </CopilotKit>
  );
}

export default App;