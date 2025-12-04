import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import useDebounce from "../hooks/useDebounce";
import axiosJWT from "../utils/axiosJWT";
import { useCopilotReadable } from '@copilotkit/react-core';
import "./PinterestAPI.css";

const RESULT_COUNT = 30;

const PinterestAPI = ({ searchQuery = "", selectedTags = [] }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [menuOpen, setMenuOpen] = useState(null);

  const pixabayAPIKey = "48656670-3136fdbaccdd21d1e52a24eb0";
  const debouncedSearch = useDebounce(searchQuery, 600);

  const queryWithTags = useMemo(
    () =>
      [debouncedSearch, ...selectedTags]
        .join(" ")
        .replace(/\s+/g, " ")
        .trim(),
    [debouncedSearch, selectedTags]
  );

   // ✅ STEP 1: Tell AI about current images
  useCopilotReadable({
    description: "Current pins displayed in the feed",
    value: images.length > 0 
      ? `Showing ${images.length} pins. Search: "${searchQuery}", Tags: ${selectedTags.join(', ') || 'none'}. Recent pins: ${images.slice(0, 3).map(img => img.title).join(', ')}`
      : `No pins displayed. Current search: "${searchQuery}"`
  });

  // ✅ STEP 2: Tell AI about search state
  useCopilotReadable({
    description: "Current search and filter settings",
    value: `Search query: "${searchQuery}", Active tags: ${selectedTags.join(', ') || 'none'}, Total results: ${images.length} pins`
  });

  useEffect(() => {
    let isMounted = true;

    const fetchImages = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await axios.get("https://pixabay.com/api/", {
          params: {
            key: pixabayAPIKey,
            q: queryWithTags || "popular",
            image_type: "photo",
            per_page: RESULT_COUNT,
          },
        });

        if (!isMounted) return;

        const formattedImages = response.data.hits.map((item) => ({
          id: item.id,
          url: item.largeImageURL,
          title: item.tags,
          user: item.user,
        }));

        setImages(formattedImages);
      } catch (err) {
        if (isMounted) {
          setError(
            "We couldn't fetch new ideas right now. Please try again in a moment."
          );
        }
        console.error("Pixabay error", err);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchImages();

    return () => {
      isMounted = false;
    };
  }, [queryWithTags]);

  const handleDownload = (url) => window.open(url, "_blank", "noopener");

  const toggleMenu = (id) =>
    setMenuOpen((prev) => (prev === id ? null : id));

  // ⭐ NEW: SAVE IMAGE FUNCTION
  const handleSave = async (img) => {
    try {
      const data = {
        image_url: img.url,
        title: img.title,
      };

      await axiosJWT.post("/api/save/", data);

      alert("Saved successfully! 🎉");
    } catch (err) {
      console.log("Save error", err);
      alert("Failed to save image.");
    }
  };

  return (
    <div className="px-4 py-6 sm:px-6 lg:px-10 imgcon">
      {loading && (
        <p className="mx-auto max-w-xl rounded-2xl bg-slate-100 px-6 py-4 text-center text-base font-medium text-slate-500">
          Finding the best ideas for you…
        </p>
      )}

      {error && !loading && (
        <p className="mx-auto max-w-xl rounded-2xl bg-rose-50 px-6 py-4 text-center text-base font-semibold text-rose-700">
          {error}
        </p>
      )}

      {!loading && !error && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {images.map((img) => (
            <div
              key={img.id}
              className="group relative aspect-[3/4] overflow-hidden rounded-3xl bg-slate-50 shadow-2xl"
            >
              <img
                src={img.url}
                alt={img.title}
                className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
              />

              <div className="absolute inset-0 flex flex-col justify-between bg-gradient-to-b from-slate-900/10 via-slate-900/20 to-slate-900/70 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      className="rounded-full bg-white/90 px-4 py-2 text-xs font-semibold text-slate-900 shadow-lg shadow-slate-900/10 transition hover:bg-white"
                      onClick={() => handleDownload(img.url)}
                    >
                      Download
                    </button>
                    <button
                      type="button"
                      className="rounded-full bg-red-600 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-red-600/40 transition hover:bg-red-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500"
                      onClick={() => handleSave(img)}
                    >
                      Save
                    </button>
                  </div>

                  <div className="relative">
                    <button
                      type="button"
                      className="flex h-11 w-11 items-center justify-center rounded-full bg-white/90 text-lg font-bold text-slate-900 shadow-lg shadow-slate-900/20 transition hover:bg-white"
                      onClick={() => toggleMenu(img.id)}
                      aria-label="More options"
                    >
                      ⋯
                    </button>
                    {menuOpen === img.id && (
                      <div className="absolute right-0 top-12 w-40 rounded-2xl bg-white p-2 shadow-xl shadow-slate-900/20">
                        <button
                          className="w-full rounded-xl px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-100"
                          type="button"
                          onClick={() => toggleMenu(null)}
                        >
                          Copy link
                        </button>
                        <button
                          className="w-full rounded-xl px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-100"
                          type="button"
                          onClick={() => toggleMenu(null)}
                        >
                          Hide pin
                        </button>
                        <button
                          className="w-full rounded-xl px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-100"
                          type="button"
                          onClick={() => toggleMenu(null)}
                        >
                          Report
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                <div className="space-y-1 text-white">
                  <h3 className="text-base font-semibold leading-tight">
                    {img.title || "Untitled idea"}
                  </h3>
                  {img.user && (
                    <span className="text-sm text-white/80">by {img.user}</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PinterestAPI;
