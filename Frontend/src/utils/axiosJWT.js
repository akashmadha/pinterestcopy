import axios from "axios";
import API_BASE_URL from "../config";

const axiosJWT = axios.create({
  baseURL: API_BASE_URL,
});

axiosJWT.interceptors.request.use(
  (config) => {
    const access =
      localStorage.getItem("accessToken") || localStorage.getItem("access");
    if (access) {
      config.headers.Authorization = `Bearer ${access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosJWT.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401, try refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refresh =
        localStorage.getItem("refreshToken") || localStorage.getItem("refresh");
      if (!refresh) return Promise.reject(error);

      try {
        const res = await axios.post(`${API_BASE_URL}/api/token/refresh/`, {
          refresh,
        });

        const newAccess = res.data.access;
        localStorage.setItem("accessToken", newAccess);

        originalRequest.headers.Authorization = `Bearer ${newAccess}`;

        return axiosJWT(originalRequest);
      } catch (err) {
        // If refresh also fails → logout
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosJWT;
