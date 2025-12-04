const isBrowser = typeof window !== "undefined";
const isLocalhost = isBrowser && window.location.hostname === "localhost";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  (isLocalhost ? "http://127.0.0.1:8000" : "https://pinterestcopy.onrender.com");

export default API_BASE_URL;

