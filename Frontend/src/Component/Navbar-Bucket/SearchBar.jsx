import React from 'react';
import PropTypes from 'prop-types';
import './SearchBar.css'; // 🎨 styling for the search bar

// ✅ Functional component that takes two props:
// - searchQuery → the current text in the input
// - setSearchQuery → function to update that text in parent state
function SearchBar({ searchQuery, setSearchQuery }) {
  return (
    <div className="search-bar">
      {/* 🔍 Input field bound to searchQuery */}
      <input
        type="text"
        placeholder="Search images..."   // Grey placeholder text
        value={searchQuery}              // Controlled input → always matches React state
        onChange={(e) => setSearchQuery(e.target.value)} 
        // ⬆️ This updates the parent state in real-time when the user types
      />
    </div>
  );
}

// 🛡️ Prop type validation (helps catch bugs in dev)
SearchBar.propTypes = {
  searchQuery: PropTypes.string.isRequired,  // must be a string
  setSearchQuery: PropTypes.func.isRequired, // must be a function
};

export default SearchBar;
