import React, { useEffect, useState } from "react";
import axiosJWT from "../../utils/axiosJWT";
import { useCopilotReadable } from '@copilotkit/react-core';

const UserProfile = () => {
  const [savedImages, setSavedImages] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchSavedImages = async () => {
    try {
      const response = await axiosJWT.get("/api/saved/");
      setSavedImages(response.data);
    } catch (error) {
      console.error("Error fetching saved images:", error);
    } finally {
      setLoading(false);
    }
  };

  // ✅ FIXED: Use ACTUAL variables from your component
  useCopilotReadable({
    description: "Current user profile information",
    value: `Saved pins: ${savedImages.length}, Loading: ${loading}`
  });

  useEffect(() => {
    fetchSavedImages();
  }, []);

  return (
    <section className="min-h-screen bg-gradient-to-b from-rose-50 via-white to-white px-4 py-10 sm:px-6 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8 flex flex-col gap-2">
          <h1 className="text-3xl font-bold text-slate-900 sm:text-4xl">
            Your Saved Pins
          </h1>
          <p className="text-base text-slate-600">
            Everything you’ve bookmarked lives here. Click a pin to view it in a
            new tab.
          </p>
        </header>

        {loading && (
          <p className="rounded-2xl bg-white px-6 py-4 text-center text-base font-medium text-slate-500 shadow">
            Loading your saved images...
          </p>
        )}

        {!loading && savedImages.length === 0 && (
          <p className="rounded-2xl bg-white px-6 py-4 text-center text-base font-semibold text-slate-600 shadow">
            You haven't saved any images yet.
          </p>
        )}

        {!loading && savedImages.length > 0 && (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {savedImages.map((item) => (
              <article
                key={item.id}
                className="group relative overflow-hidden rounded-3xl bg-white shadow-xl transition hover:-translate-y-1 hover:shadow-2xl"
              >
                <a href={item.image.image_url} target="_blank" rel="noreferrer">
                  <img
                    src={item.image.image_url}
                    alt={item.image.title || "Saved"}
                    className="h-64 w-full object-cover transition duration-500 group-hover:scale-105"
                  />
                </a>
                <div className="p-4">
                  <p className="text-base font-semibold text-slate-900">
                    {item.image.title || "Untitled Image"}
                  </p>
                  <p className="text-sm text-slate-500">{item.image.user}</p>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

export default UserProfile;
