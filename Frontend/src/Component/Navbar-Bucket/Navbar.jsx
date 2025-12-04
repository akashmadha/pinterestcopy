import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom"; // For navigation
import { ChevronDown } from "lucide-react"; // Dropdown icon
import "./navbar.css"; // CSS for styling
import SearchBar from "./SearchBar"; // Search input component
import Profile from "./Profile"; // Profile avatar/info
import FilterChips from "./FilterChips"; // Tag filter buttons
import UserProfile from "./UserProfile";
import { useCopilotReadable } from '@copilotkit/react-core';

// ✅ Props are passed from parent (App.jsx usually)
// These handle search + selected tags state
function Navbar({
  searchQuery,
  setSearchQuery,
  selectedTags,
  setSelectedTags,
}) {
  // 🔽 Local state for dropdown (profile menu)
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  // 📱 Local state for mobile menu toggle
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  // 🧭 React Router hook to navigate between pages
  const navigate = useNavigate();
  // 👤 Store user details fetched from <Profile />
  const [userDetails, setUserDetails] = useState(null);

  // 🔁 Toggles dropdown visibility
  const toggleDropdown = () => setIsDropdownOpen(!isDropdownOpen);
  // 🔁 Toggles mobile menu visibility
  const toggleMobileMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);

  useCopilotReadable({
  description: "Current navbar and search state",
  value: `Search: "${searchQuery || ''}", Tags: ${(selectedTags || []).join(', ') || 'none'}, Dropdown: ${isDropdownOpen ? 'open' : 'closed'}, Mobile menu: ${isMobileMenuOpen ? 'open' : 'closed'}, User: ${userDetails ? userDetails.username : 'not loaded'}`
});
  
  // 🧠 Close dropdown automatically when clicking outside
  React.useEffect(() => {
    const closeDropdown = (event) => {
      // if click is not inside ".profile-section" → close dropdown
      if (!event.target.closest(".profile-section")) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener("click", closeDropdown);
    // cleanup on unmount
    return () => document.removeEventListener("click", closeDropdown);
  }, []);

  // ================================
  // 🧱 JSX Structure
  // ================================
  return (
    <nav className="top-nav">
      <section className="m-tpnav">
        <div className="m-tn-inside">

          {/* 🔍 Search and filter section */}
          <div className="search-filter-section">
            {/* Search bar input */}
            <SearchBar
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
            />
            {/* Filter chips like “Nature”, “Animals”, etc. */}
            <FilterChips
              selectedTags={selectedTags}
              setSelectedTags={setSelectedTags}
            />
          </div>

          {/* 👤 Right side of navbar (profile & dropdown) */}
          <div className={`nav-container ${isMobileMenuOpen ? "open" : ""}`}>
            <div className="profile-section">
              {/* Small profile circle */}
              <Profile onUserData={(data) => setUserDetails(data)} />

              {/* Dropdown toggle button (chevron icon) */}
              <button className="profile-button" onClick={toggleDropdown}>
                <ChevronDown size={24} />
              </button>

              {/* Conditional render: dropdown only visible if open */}
              {isDropdownOpen && (
                <div className="dropdown-menu">
                  <div className="m-ci">Currently in</div>
                  <div className="user-info">
                    <div className="user-initial">
                      {(userDetails?.initial ||
                        userDetails?.username ||
                        userDetails?.email ||
                        "?")
                        .charAt(0)
                        .toUpperCase()}
                    </div>
                    <div className="user-details">
                      <p className="username">
                        {userDetails?.displayName ||
                          userDetails?.username ||
                          "Loading..."}
                      </p>
                      <p className="email">
                        {userDetails?.email || "Fetching email..."}
                      </p>
                    </div>
                  </div>
                  <ul>

                    {/* 🔧 Dropdown links */}
                    <li>
                      <Link to="/settings">Settings</Link>
                    </li>
                    <li>
                      <Link to="/logout">Logout</Link>
                    </li>
                     <li>
                      <Link to="/UserProfile">UserProfile</Link>
                    </li>
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
    </nav>
  );
}

export default Navbar;
