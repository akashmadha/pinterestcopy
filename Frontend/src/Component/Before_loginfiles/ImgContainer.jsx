import React, { useState, useEffect, useRef } from "react";
import "./ImgContainer.css";
import { useCopilotReadable } from "@copilotkit/react-core";

import img1 from "../../assets/images/img1.jpg";
import img2 from "../../assets/images/img2.jpg";
import img3 from "../../assets/images/img3.jpg";
import img4 from "../../assets/images/img4.jpg";
import img5 from "../../assets/images/img5.jpg";
import img6 from "../../assets/images/img6.jpg";
import img7 from "../../assets/images/img7.jpg";
import img8 from "../../assets/images/img8.jpg";

import ib1 from "../../assets/images/ib1.jpg";
import ib2 from "../../assets/images/ib2.jpg";
import ib3 from "../../assets/images/ib3.jpg";
import ib4 from "../../assets/images/ib4.jpg";
import ib5 from "../../assets/images/ib5.jpg";
import ib6 from "../../assets/images/ib6.jpg";
import ib7 from "../../assets/images/ib7.jpg";

const PLACEHOLDER =
  'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><rect width="100%" height="100%" fill="%23eee"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="%23999" font-size="24">image missing</text></svg>';

function ImgContainer() {
  const slides = [
    { text: "Action Time Fight Idea", images: [img1, img2, img3, img4] },
    { text: "Evening Ark Drive", images: [img5, img6, img7, img8] },
    { text: "Weekend Brunch FightTown", images: [img2, img4, img6, img8] },
    { text: "Festive Dessert Inspiration", images: [img1, img3, img5, img7] },
  ];

  const slide = [
    { text: "Chai Time Snacks Idea", images: [ib1, ib2, ib3, ib4] },
    { text: "Evening Tea Recipes", images: [ib2, ib1, ib4, ib6] },
    { text: "Weekend Brunch Recipes", images: [ib7, ib4, ib2, ib3] },
    { text: "Festive Dessert Inspiration", images: [ib5, ib6, ib7, ib1] },
  ];

  const [current, setCurrent] = useState(0);
  const [fade, setFade] = useState(false);
  const timeoutRef = useRef(null);

  // 🟢 FIXED: useCopilotReadable placed AFTER declarations
  useCopilotReadable({
    description: "Hero image carousel state",
    value: `Slide ${current + 1}/${slides.length} | Title: "${slides[current].text}" | Fade: ${
      fade ? "active" : "inactive"
    }`,
  });

  // Preload images
  useEffect(() => {
    [...slides, ...slide]
      .flatMap((s) => s.images)
      .forEach((src) => {
        const img = new Image();
        img.src = src;
      });
  }, []);

  // 🟢 FIXED: Only ONE rotating effect
  useEffect(() => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);

    timeoutRef.current = setTimeout(() => {
      setFade(true);

      setTimeout(() => {
        setCurrent((prev) => (prev + 1) % slides.length);
        setFade(false);
      }, 400); // fade duration
    }, 2000);

    return () => clearTimeout(timeoutRef.current);
  }, [current]);

  return (
    <main className="main-wrap">
      <div className="hero-container">
        <h1 className="hero-title">Get your next</h1>

        {/* Text fade animation */}
        <div className={`hero-subtitle ${fade ? "fade-out" : "fade-in"}`}>
          <h2 key={current} className="subtitle-text">
            {slides[current].text}
          </h2>
        </div>

        {/* Dots */}
        <div className="dots-container">
          {slides.map((_, i) => (
            <button
              key={i}
              className={`slide-dot ${i === current ? "active" : ""}`}
              onClick={() => setCurrent(i)}
              aria-label={`Go to slide ${i + 1}`}
            />
          ))}
        </div>

        {/* FIRST Image Group */}
        <div className="groups-wrapper">
          <div className={`images-group fade ${fade ? "fade-out" : "fade-in"}`}>
            {slides[current].images.map((src, j) => (
              <div className="image-bucket" key={j}>
                <img src={src || PLACEHOLDER} draggable="false" />
              </div>
            ))}
          </div>
        </div>

        {/* SECOND Image Group */}
        <div className="ab-headwrap">
          <div className="ab-wrapper">
            <div
              className={`images-group fade ${fade ? "fade-out" : "fade-in"}`}
            >
              {slide[current].images.map((src, j) => (
                <div className="ib-two" key={j}>
                  <img src={src || PLACEHOLDER} draggable="false" />
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="how-it-works">
          <a href="#scroll-target" className="how-btn">
            Here's how it works <span className="arrow">↓</span>
          </a>
        </div>
      </div>
    </main>
  );
}

export default ImgContainer;
