import React, { useState } from "react";
import PinterestAPI from "../PinterestAPI";
import "./Explore.css";

import natureImg from "../../assets/images/nature.jpg";
import animalsImg from "../../assets/images/animals.jpg";
import foodImg from "../../assets/images/food.jpg";
import travelImg from "../../assets/images/travel.jpg";
import techImg from "../../assets/images/tech.jpg";
import peopleImg from "../../assets/images/people.jpg";

// Get current date/time (formatted nicely, e.g. "November 26, 2025")
const now = new Date();
const currentDate = now.toLocaleDateString("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
});
const currentTime = now.toLocaleTimeString([], {
  hour: "2-digit",
  minute: "2-digit",
});

const topics = [
  { name: "Nature", img: natureImg },
  { name: "Animals", img: animalsImg },
  { name: "Food", img: foodImg },
  { name: "Travel", img: travelImg },
  { name: "Technology", img: techImg },
  { name: "People", img: peopleImg }
];

export default function Explore() {
  const [selectedTopic, setSelectedTopic] = useState("");

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-8 sm:px-8">
      {/* Top Date / Time Box */}
      <div className="mx-auto mb-8 max-w-6xl text-center">
        <div className="inline-flex flex-col items-center rounded-3xl bg-white px-8 py-4 shadow-md shadow-slate-200">
          <h2 className="text-xl font-semibold text-slate-900">
            {currentDate}
          </h2>
          <p className="mt-1 text-sm font-medium text-slate-500">
            {currentTime} · Stay inspired, keep exploring.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl">
        {/* If no topic selected → show large topic cards */}
        {!selectedTopic && (
          <>
            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {topics.map((topic) => (
                <button
                  key={topic.name}
                  type="button"
                  onClick={() => setSelectedTopic(topic.name)}
                  className="group relative h-52 overflow-hidden rounded-3xl bg-slate-200 text-left shadow-xl shadow-slate-300 transition-transform duration-300 hover:-translate-y-1 hover:shadow-2xl"
                  style={{ backgroundImage: `url(${topic.img})` }}
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-slate-900/40 via-slate-900/20 to-slate-900/60" />
                  <div className="relative flex h-full w-full items-center px-8">
                    <p className="text-2xl font-extrabold tracking-wide text-white drop-shadow-md">
                      {topic.name}
                    </p>
                  </div>
                </button>
              ))}
            </div>
            <p className="mt-10 text-center text-lg text-slate-500">
              Click a topic to load images
            </p>
          </>
        )}

        {/* After clicking → hide topic cards, only show results */}
        {selectedTopic && (
          <>
            <div className="mb-4 flex items-center justify-between">
              <button
                type="button"
                onClick={() => setSelectedTopic("")}
                className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50"
              >
                <span aria-hidden="true">←</span>
                Back to topics
              </button>
              <p className="text-sm text-slate-500">
                Showing ideas for <span className="font-semibold">{selectedTopic}</span>
              </p>
            </div>
            <div className="mt-2">
              <PinterestAPI searchQuery={selectedTopic} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
