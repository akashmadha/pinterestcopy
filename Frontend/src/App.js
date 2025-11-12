import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";

// 🧱 Authentication components
import Register from "./Component/sign_up_pages/Register";
import Login from "./Component/sign_up_pages/Login";
import Logout from "./Component/sign_up_pages/Logout";

// 🧭 Layout + UI components
import Navbar from "./Component/Navbar-Bucket/Navbar";
import Sidebar from "./Component/Navbar-Bucket/Sidebar";
import Navigation from "./Component/Navbar-Bucket/Navigation";
import PinterestAPI from "./Component/PinterestAPI";
import Profile from "./Component/Navbar-Bucket/Profile";

// 🧩 Sidebar-linked routes
import Create from './Component/sidebar_buttons/Create';
import Explore from './Component/sidebar_buttons/Explore';
import Messages from './Component/sidebar_buttons/Messages';
import Home from './Component/Home';
import Notifications from './Component/sidebar_buttons/Notifications';

function App() {
  // ✅ Track if the user is logged in
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // ✅ Search + tags state shared between Navbar & PinterestAPI
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);

  // 🧭 useLocation helps determine the current route
  const location = useLocation();

  // 🧾 Define pages where the sidebar/navbar should be hidden
  const pagesWithoutSidebarNavbar = [
    "/explore",
    "/create",
    "/messages",
    "/notifications",
    "/Profile",
    "/login",
    "/register",
  ];

  // ⚙️ Boolean — true if current page is in the "hide" list
  const hideSidebarNavbar = pagesWithoutSidebarNavbar.includes(location.pathname);

  // 🧩 Whenever the URL changes, check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    setIsAuthenticated(!!token); // Convert token existence → boolean
  }, [location.pathname]);

  // ============================================================
  // 🚀 RETURN: Decide between Authenticated vs Unauthenticated UI
  // ============================================================

  return (
    <>
      {!isAuthenticated ? (
        // ----------------------------
        // 👤 NOT LOGGED IN
        // ----------------------------
        <>
          {/* Top navigation bar (likely includes logo/login buttons) */}
          <Navigation setIsAuthenticated={setIsAuthenticated} />

          {/* Main page layout for unauthenticated users */}
          <div
            style={{
              paddingTop: "80px",
              minHeight: "100vh",
              backgroundColor: "#f7f7f7",
            }}
          >
            <Routes>
              {/* 🪪 Auth routes */}
              <Route
                path="/login"
                element={<Login setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/register"
                element={<Register setIsAuthenticated={setIsAuthenticated} />}
              />
              {/* Any other route redirects to login */}
              <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
          </div>
        </>
      ) : (
        // ----------------------------
        // 🔒 LOGGED IN LAYOUT
        // ----------------------------
        <>
          {/* Sidebar visible for navigation */}
          <Sidebar />

          {/* Conditional rendering: Hide navbar + Pinterest feed if not needed */}
          {!hideSidebarNavbar && (
            <div className="pin_nav_continer">
              {/* 🧭 Navbar controls search and filter */}
              <Navbar
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                selectedTags={selectedTags}
                setSelectedTags={setSelectedTags}
              />

              {/* 🖼️ Pinterest-style image feed based on search + tags */}
              <PinterestAPI
                searchQuery={searchQuery}
                selectedTags={selectedTags}
              />
            </div>
          )}

          {/* 🚦 App routes (pages linked from sidebar) */}
          <Routes>
            <Route path="/home" element={<Home />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/explore" element={<Explore />} />
            <Route path="/create" element={<Create />} />
            <Route path="/messages" element={<Messages />} />
            <Route path="/register" element={<Register />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route
              path="/logout"
              element={<Logout setIsAuthenticated={setIsAuthenticated} />}
            />
            {/* Default redirect if route doesn’t match */}
            <Route path="*" element={<Navigate to="/home" />} />
          </Routes>
        </>
      )}
    </>
  );
}

export default App;
