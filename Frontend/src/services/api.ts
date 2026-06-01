// services/api.ts
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import router from '../router/index.ts';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Интерцептор запросов: добавляем токен в заголовки
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Интерцептор ответов: обрабатываем ошибки авторизации
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Токен истёк или невалиден — разлогиниваем
      const authStore = useAuthStore();
      authStore.logout();
      router.push({ name: 'AuthLogin' });
    }
    return Promise.reject(error);
  }
);

export default api;