import React from "react";
import PropTypes from "prop-types";
import "./FilterChips.css"; // optional styling file
import { useCopilotReadable } from '@copilotkit/react-core';

function FilterChips({ selectedTags = [], setSelectedTags = () => {} }) {
  const tags = ["Nature", "Animals", "Food", "Travel", "Technology", "People"];


   // ✅ ADD THIS: Share filter state with AI
  useCopilotReadable({
    description: "Current filter tags state",
    value: `Available tags: ${tags.join(', ')}, Active filters: ${selectedTags.join(', ') || 'none'}`
  });


  const toggleTag = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  return (
    <div className="filter-chips">
      {tags.map((tag) => (
        <button
          key={tag}
          className={`chip ${selectedTags.includes(tag) ? "active" : ""}`}
          onClick={() => toggleTag(tag)}
        >
          {tag}
        </button>
      ))}
    </div>
  );
}

FilterChips.propTypes = {
  selectedTags: PropTypes.array,
  setSelectedTags: PropTypes.func,
};

export default FilterChips;
