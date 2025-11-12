import React, { useState, useEffect } from "react";
import axios from "axios";
import useDebounce from "../hooks/useDebounce"; // ✅ custom hook to delay the API call while typing
import "./PinterestAPI.css";

// ✅ Main component that fetches and displays images
function PinterestAPI({ searchQuery = "", selectedTags = [] }) {
  // --------------------
  // 🧠 STATE VARIABLES
  // --------------------
  const [images, setImages] = useState([]);     // stores list of fetched images
  const [loading, setLoading] = useState(false); // true while API is fetching
  const [error, setError] = useState(null);      // stores error messages if fetch fails

  // ✅ Pixabay API key
  const pixabayAPIKey = "48656670-3136fdbaccdd21d1e52a24eb0";

  // --------------------
  // ⏳ DEBOUNCE LOGIC
  // --------------------
  // useDebounce delays updates to searchQuery by 600ms
  // This means the API won't run until the user stops typing for 600ms
  const debouncedSearch = useDebounce(searchQuery, 600);

  // --------------------
  // 🔍 FETCH IMAGES FUNCTION
  // --------------------
  const fetchImages = async () => {
    // 🧩 Step 1: If nothing is searched and no tags are selected, clear results
    if (!debouncedSearch && selectedTags.length === 20) {
      setImages([]);
      return;
    }

    // 🧩 Step 2: Prepare for API call
    setLoading(true);
    setError(null);

    try {
      // Combine search text + selected tags into one query string
      const q = [debouncedSearch, ...selectedTags].join(" ");

      // 🧩 Step 3: Make GET request to Pixabay API
      const res = await axios.get("https://pixabay.com/api/", {
        params: {
          key: pixabayAPIKey, // your API key
          q,                  // query (keywords)
          image_type: "photo",
          per_page: 30,       // number of images per fetch
          orientation: "horizontal",
        },
      });

      // 🧩 Step 4: Extract useful data (id, url, title) from response
      const imgs = res.data.hits.map((item) => ({
        id: item.id,
        url: item.largeImageURL,
        title: item.tags,
      }));

      // ✅ Save fetched images to state
      setImages(imgs);

    } catch (err) {
      // ❌ Catch and display any fetch errors
      setError("Error fetching images: " + err.message);
    } finally {
      // ✅ Always stop loading state (success or error)
      setLoading(false);
    }
  };

  // --------------------
  // 🔁 SIDE EFFECT (fetch data)
  // --------------------
  useEffect(() => {
    // Runs fetchImages whenever:
    // - debouncedSearch (after typing stops)
    // - selectedTags (filter chips) changes
    // - searchQuery changes
    fetchImages();
  }, [debouncedSearch, searchQuery, selectedTags]);

  // --------------------
  // 🎨 RENDER UI
  // --------------------
  return (
    <div className="gallery-container">
      {/* Show loading, error, or images */}
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <div className="image-grid">
          {images.map((img) => (
            <div key={img.id} className="image-card">
              <img src={img.url} alt={img.title} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PinterestAPI;
