import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 120000, // 2 minutes timeout for evaluation requests
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`, config.data);
    return config;
  },
  (error) => {
    console.error("❌ Request interceptor error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error(`❌ API Error (${error.response.status}):`, error.response.data);
      console.error("Request was:", error.config?.method?.toUpperCase(), error.config?.url);
    } else if (error.request) {
      // Request made but no response
      console.error("❌ Network Error (no response):", error.message);
      console.error("Request was:", error.config?.method?.toUpperCase(), error.config?.url);
    } else {
      // Something else happened
      console.error("❌ Error:", error.message);
    }
    return Promise.reject(error);
  }
);
