// stores/auth.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '../services/auth';
import type { UserLogin, UserCreate, UserResponse } from '../types/auth';

export const useAuthStore = defineStore('auth', () => {
  // ===== Константы =====
  const TOKEN_KEY = 'access_token';
  const USER_KEY = 'user_data';

  // ===== Состояние =====
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY));
  const user = ref<UserResponse | null>(loadUser());
  const loading = ref(false);
  const error = ref<string | null>(null);

  // ===== Геттеры =====
  const isAuthenticated = computed(() => !!token.value);
  const currentUser = computed(() => user.value);

  // ===== Приватные методы =====
  function loadUser(): UserResponse | null {
    try {
      const savedUser = localStorage.getItem(USER_KEY);
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  }

  function saveAuth(accessToken: string) {
    token.value = accessToken;
    localStorage.setItem(TOKEN_KEY, accessToken);
  }

  function clearAuth() {
    token.value = null;
    user.value = null;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  // ===== Публичные методы =====
  /**
   * Вход в систему
   */
  async function login(credentials: UserLogin) {
    loading.value = true;
    error.value = null;

    try {
      const tokenResponse = await authService.login(credentials);
      saveAuth(tokenResponse.access_token);

      // После логина получаем профиль пользователя
      await fetchProfile();

      return true;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка входа';
      return false;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Регистрация нового пользователя
   */
  async function register(userData: UserCreate) {
    loading.value = true;
    error.value = null;

    try {
      const tokenResponse = await authService.register(userData);
      saveAuth(tokenResponse.access_token);

      // После регистрации получаем профиль
      await fetchProfile();

      return true;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка регистрации';
      return false;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Получить профиль текущего пользователя
   */
  async function fetchProfile() {
    if (!token.value) return;

    try {
      const userData = await authService.getProfile();
      user.value = userData;
      localStorage.setItem(USER_KEY, JSON.stringify(userData));
    } catch (err: any) {
      console.error('Ошибка загрузки профиля:', err);
      // Если не удалось загрузить профиль — токен невалиден
      if (err.response?.status === 401) {
        clearAuth();
      }
    }
  }

  /**
   * Проверка валидности токена при загрузке приложения
   */
  async function checkAuth() {
    if (!token.value) return false;

    try {
      await fetchProfile();
      return isAuthenticated.value;
    } catch {
      return false;
    }
  }

  /**
   * Выход из системы
   */
  function logout() {
    clearAuth();
  }

  /**
   * Сброс ошибки
   */
  function clearError() {
    error.value = null;
  }

  return {
    // Состояние
    token,
    user,
    loading,
    error,

    // Геттеры
    isAuthenticated,
    currentUser,

    // Действия
    login,
    register,
    logout,
    checkAuth,
    fetchProfile,
    clearError,
  };
});