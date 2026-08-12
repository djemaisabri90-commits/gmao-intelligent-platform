// src/api/client.ts
import axios from "axios";
import { getAccessToken, setTokens, clearTokens } from "./auth";
import toast from "react-hot-toast";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

// ✅ Nouveau client pour l’API predictive
export const predictiveClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL_PREDICTIVE,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

// Intercepteur commun : ajout du token
const attachTokenInterceptor = (client: typeof apiClient) => {
  client.interceptors.request.use((config) => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  client.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          const refresh = localStorage.getItem("refresh_token");
          const { data } = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/token/refresh/`,
            { refresh }
          );
          setTokens(data.access, data.refresh);
          originalRequest.headers.Authorization = `Bearer ${data.access}`;
          return client(originalRequest);
        } catch (refreshError) {
          clearTokens();
          window.location.href = "/login";
          return Promise.reject(refreshError);
        }
      }
      return Promise.reject(error);
    }
  );

  client.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 500) {
        toast.error("Erreur interne du serveur");
      } else if (error.response?.status === 403) {
        toast.error("Permission refusée");
      }
      return Promise.reject(error);
    }
  );
};

// ✅ Attacher les intercepteurs aux deux clients
attachTokenInterceptor(apiClient);
attachTokenInterceptor(predictiveClient);
