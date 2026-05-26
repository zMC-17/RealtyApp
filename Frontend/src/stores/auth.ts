/**
 * Pinia хранилище для управления пользователем и аутентификацией
 *
 * Реализует mock JWT аутентификацию:
 * - Вход/выход с fake JWT tokens
 * - Сохранение токена в localStorage
 * - Восстановление сеанса при перезагрузке приложения
 * - Переключение между ролями (владелец/арендатор)
 *
 * Готово для замены на реальный API без изменений интерфейса
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { UserRole, AuthSession, User } from '../shared/types';

const STORAGE_KEY = 'auth_session';
const TOKEN_PREFIX = 'mock_jwt_';

/**
 * Генерирует fake JWT token для mock аутентификации
 * Формат: mock_jwt_<base64(userId+timestamp)>
 */
const generateMockToken = (userId: string): string => {
  const payload = `${userId}:${Date.now()}`;
  const encoded = btoa(payload);
  return `${TOKEN_PREFIX}${encoded}`;
};

/**
 * Mock база данных пользователей для аутентификации
 * Используется для демонстрации и testing
 */
const MOCK_USERS: Record<string, User> = {
  landlord_user: {
    id: 'user_1',
    email: 'landlord@example.com',
    username: 'landlord_user',
    password_hash: 'hashed_password_123', // Fake hash для demo
    created_at: '2024-01-01T00:00:00Z',
  },
  tenant_user: {
    id: 'user_3',
    email: 'tenant@example.com',
    username: 'tenant_user',
    password_hash: 'hashed_password_456',
    created_at: '2024-01-05T00:00:00Z',
  },
};

/**
 * Validate mock credentials
 * В реальном приложении это было бы запросом к backend API
 */
const validateCredentials = (username: string): User | null => {
  const user = MOCK_USERS[username];
  if (user) {
    // Simulate network delay
    return user;
  }
  return null;
};

export const useAuthStore = defineStore('auth', () => {
  // State
  const session = ref<AuthSession | null>(null);
  const currentRole = ref<UserRole>('landlord');
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const isAuthenticated = computed(() => session.value !== null);
  const user = computed(() => session.value?.user ?? null);
  const accessToken = computed(() => session.value?.access_token ?? null);

  // ============================================================
  // Private Helper Actions
  // ============================================================

  /**
   * Сохранить сеанс в localStorage
   */
  const persistSession = (newSession: AuthSession) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(newSession));
    } catch (err) {
      console.error('Failed to persist session:', err);
    }
  };

  /**
   * Удалить сеанс из localStorage
   */
  const clearPersistedSession = () => {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (err) {
      console.error('Failed to clear persisted session:', err);
    }
  };

  /**
   * Восстановить сеанс из localStorage
   */
  const restoreSession = () => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const restoredSession: AuthSession = JSON.parse(stored);
        session.value = restoredSession;
        currentRole.value = restoredSession.current_role;
      }
    } catch (err) {
      console.error('Failed to restore session:', err);
      clearPersistedSession();
    }
  };

  // ============================================================
  // Public Actions
  // ============================================================

  /**
   * Вход в систему с mock JWT аутентификацией
   * 
   * @param username Имя пользователя (landlord_user или tenant_user)
   * @param _password Пароль (игнорируется в mock режиме)
   * 
   * MOCK УЧЁТНЫЕ ДАННЫЕ:
   * - landlord_user / любой пароль
   * - tenant_user / любой пароль
   */
  const login = async (username: string, _password: string): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;

    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 500));

      // Validate mock credentials
      const mockUser = validateCredentials(username);
      if (!mockUser) {
        error.value = 'Неверное имя пользователя или пароль';
        return false;
      }

      // Generate mock JWT token
      const accessToken = generateMockToken(mockUser.id);

      // Create session
      const newSession: AuthSession = {
        user: mockUser,
        access_token: accessToken,
        current_role: 'landlord', // Default role
      };

      // Save to state and localStorage
      session.value = newSession;
      currentRole.value = newSession.current_role;
      persistSession(newSession);

      return true;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка входа';
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Регистрация нового пользователя (mock, не реализовано)
   * В реальном приложении создавал бы нового пользователя на backend
   */
  const register = async (username: string, _password: string): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;

    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 500));

      // Mock: проверяем что пользователя ещё нет
      const existing = validateCredentials(username);
      if (existing) {
        error.value = 'Пользователь с таким именем уже существует';
        return false;
      }

      // Mock: просто логируем, регистрация не реальная
      console.log('Mock register:', username);
      error.value = 'Регистрация пока не реализована. Используйте landlord_user или tenant_user';
      return false;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка регистрации';
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Переключение между ролями владельца и арендатора
   */
  const switchRole = (role: UserRole) => {
    currentRole.value = role;
    if (session.value) {
      session.value.current_role = role;
      persistSession(session.value);
    }
  };

  /**
   * Выход из системы
   */
  const logout = () => {
    session.value = null;
    currentRole.value = 'landlord';
    error.value = null;
    clearPersistedSession();
  };

  /**
   * Установка сеанса (используется при восстановлении сеанса из хранилища)
   * Внутренний метод для hydration
   */
  const setSession = (newSession: AuthSession) => {
    session.value = newSession;
    currentRole.value = newSession.current_role;
    persistSession(newSession);
  };

  /**
   * Инициализация хранилища (восстановление сеанса при загрузке приложения)
   * Должен быть вызван в main.ts после создания Pinia
   */
  const initializeAuth = () => {
    restoreSession();
  };

  return {
    // State
    session,
    currentRole,
    isLoading,
    error,

    // Computed
    isAuthenticated,
    user,
    accessToken,

    // Actions
    login,
    register,
    switchRole,
    logout,
    setSession,
    initializeAuth,
  };
});
