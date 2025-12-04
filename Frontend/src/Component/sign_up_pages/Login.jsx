import { useState } from "react";
import { useNavigate } from "react-router-dom";
import ImgContainer from "../Before_loginfiles/ImgContainer";
import SearchIdea from "../Before_loginfiles/SearchIdea";
import WtpSp from "../Before_loginfiles/WtpSp";
import Footer from "../Before_loginfiles/Footer";
import API_BASE_URL from "../../config";
import { useCopilotReadable } from "@copilotkit/react-core";

const Login = ({ setIsAuthenticated }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  useCopilotReadable({
    description: "Login page state",
    value: `Username: ${username || "empty"}`,
  });

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      console.log("🔄 Attempting login...");
      
      const response = await fetch(`${API_BASE_URL}/api/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      console.log("📦 Response status:", response.status);
      
      // Check if response has content before parsing
      const text = await response.text();
      console.log("📦 Raw response:", text);
      
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        console.error("❌ Failed to parse JSON:", e);
        alert("Invalid response from server. Please try again.");
        return;
      }
      
      console.log("📦 Parsed response data:", data);

      if (response.ok && data.access) {
        // ✅ Store tokens & basic profile info in localStorage
        localStorage.setItem("accessToken", data.access);
        if (data.refresh) {
          localStorage.setItem("refreshToken", data.refresh);
        }
        localStorage.setItem(
          "userProfile",
          JSON.stringify({
            username,
            email: data.email || "",
          })
        );
        
        // ✅ Debug: Verify storage
        console.log("💾 Tokens stored in localStorage:");
        console.log("Access Token:", localStorage.getItem("accessToken"));
        console.log("Refresh Token:", localStorage.getItem("refreshToken"));
        
        // Set authenticated state before navigating
        setIsAuthenticated(true);
        
        // ✅ Show success message
        alert("Login successful! ✅");
        
        // Navigate to home page
        navigate("/home");
      } else {
        alert(data.error || "Invalid credentials! ❌");
      }
    } catch (error) {
      console.error("❌ Network error:", error);
      alert("Network error. Please try again.");
    }
  };

  return (
    <div>
      <ImgContainer />
      <SearchIdea />
      <WtpSp
        username={username}
        setUsername={setUsername}
        password={password}
        setPassword={setPassword}
        onSubmit={handleLogin}
      />
      <Footer />
    </div>
  );
};

export default Login;