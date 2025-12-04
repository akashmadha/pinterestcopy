import React, { useState } from "react";
import { FaEye, FaEyeSlash, FaGoogle } from "react-icons/fa";
import { useCopilotReadable } from "@copilotkit/react-core";
import "./WtpSp.css";
import img1 from "../../assets/images/img1.jpg";
import img2 from "../../assets/images/img2.jpg";
import img3 from "../../assets/images/img3.jpg";
import img4 from "../../assets/images/img4.jpg";
import img5 from "../../assets/images/img5.jpg";
import img6 from "../../assets/images/img6.jpg";
import img7 from "../../assets/images/img7.jpg";
import img8 from "../../assets/images/img8.jpg";

// Main login card shown under the hero.
// It uses parent's username/password and submit handler.
function WtpSp({ username, setUsername, password, setPassword, onSubmit }) {
  const [showPassword, setShowPassword] = useState(false);
  const images = [img1, img2, img3, img4, img5, img6, img7, img8];

  useCopilotReadable({
    description: "Welcome to Pinterest login/signup section",
    value: `Password visibility: ${showPassword ? "visible" : "hidden"}, Username: ${
      username || "empty"
    }`,
  });

  return (
    <section className="signup-section">
      <div className="signup-container">
        {/* Left side with image grid */}
        <div className="signup-image-grid">
          <div className="image-grid2">
            {images.map((image, index) => (
              <div key={index} className="image-box">
                <img src={image} alt={`Food inspiration ${index + 1}`} className="image" />
              </div>
            ))}
          </div>
          <div className="image-overlay" />
        </div>

        {/* Right side with sign-up form */}
        <div className="signup-form-container">
          <h2 className="signup-title">Welcome to Pinterest</h2>
          <p className="signup-subtitle">Find new ideas to try</p>
          <form
            className="signup-form"
            onSubmit={onSubmit}
          >
            <div>
              <input
                type="text"
                placeholder="Email or username"
                className="input-field"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="password-field">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                className="input-field"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button 
                type="button" 
                onClick={() => setShowPassword(!showPassword)} 
                className="password-toggle"
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
           
            <button type="submit" className="continue_button">
              Continue
            </button>
            <div className="separator">
              <div className="line"></div>
              <span className="or-text">OR</span>
            </div>
            <p className="terms-text">
              By continuing, you agree to Pinterest's Terms of Service and acknowledge that you've read our Privacy Policy, Notice at collection.
            </p>
            <p className="login-text">
              Already a member? <span className="login-link">Log in</span>
            </p>
          </form>
        </div>
      </div>
    </section>
  );
}

export default WtpSp;
