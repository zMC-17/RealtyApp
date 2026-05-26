<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1 class="auth-title">RealtyApp</h1>
      <p class="auth-subtitle">Информационная система управления арендой недвижимости</p>

      <!-- Форма входа -->
      <div v-if="!showRegister" class="auth-form">
        <h2>Вход в систему</h2>

        <div class="form-group">
          <label for="login-username">Имя пользователя</label>
          <input
            id="login-username"
            v-model="loginForm.username"
            type="text"
            placeholder="landlord_user"
            @keyup.enter="handleLogin"
          />
        </div>

        <div class="form-group">
          <label for="login-password">Пароль</label>
          <input
            id="login-password"
            v-model="loginForm.password"
            type="password"
            placeholder="••••••••"
            @keyup.enter="handleLogin"
          />
        </div>

        <button class="btn-primary" :disabled="authStore.isLoading" @click="handleLogin">
          {{ authStore.isLoading ? 'Загрузка...' : 'Войти' }}
        </button>

        <div class="demo-credentials">
          <p class="demo-title">Demo учётные данные:</p>
          <p><strong>Владелец:</strong> landlord_user</p>
          <p><strong>Арендатор:</strong> tenant_user</p>
          <p><strong>Пароль:</strong> любой</p>
        </div>
      </div>

      <!-- Форма регистрации -->
      <div v-else class="auth-form">
        <h2>Создать аккаунт</h2>

        <div class="form-group">
          <label for="register-username">Имя пользователя</label>
          <input
            id="register-username"
            v-model="registerForm.username"
            type="text"
            placeholder="your_username"
          />
        </div>

        <div class="form-group">
          <label for="register-password">Пароль</label>
          <input
            id="register-password"
            v-model="registerForm.password"
            type="password"
            placeholder="••••••••"
          />
        </div>

        <div class="form-group">
          <label for="register-password-confirm">Подтверждение пароля</label>
          <input
            id="register-password-confirm"
            v-model="registerForm.passwordConfirm"
            type="password"
            placeholder="••••••••"
          />
        </div>

        <button class="btn-primary" :disabled="authStore.isLoading" @click="handleRegister">
          {{ authStore.isLoading ? 'Загрузка...' : 'Зарегистрироваться' }}
        </button>

        <p class="form-hint">
          Уже есть аккаунт?
          <button class="link-btn" @click="showRegister = false">
            Войти
          </button>
        </p>
      </div>

      <!-- Сообщение об ошибке -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Страница аутентификации (вход/регистрация)
 *
 * Mock JWT аутентификация:
 * - Демо учётные данные: landlord_user и tenant_user
 * - Token сохраняется в localStorage
 * - Сеанс восстанавливается при перезагрузке приложения
 * - После успешного входа редирект на /app/landlord/properties
 */

import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// UI state
const showRegister = ref(false);
const errorMessage = ref('');

// Form data
const loginForm = ref({
  username: '',
  password: '',
});

const registerForm = ref({
  username: '',
  password: '',
  passwordConfirm: '',
});

/**
 * Обработка входа
 * Использует mock JWT аутентификацию через auth store
 */
const handleLogin = async () => {
  errorMessage.value = '';

  if (!loginForm.value.username || !loginForm.value.password) {
    errorMessage.value = 'Пожалуйста, заполните все поля';
    return;
  }

  const success = await authStore.login(loginForm.value.username, loginForm.value.password);

  if (success) {
    // Успешный вход - редирект на главную страницу
    router.push({ name: 'LandlordProperties' });
  } else {
    // Ошибка входа - использовать сообщение об ошибке из auth store
    errorMessage.value = authStore.error || 'Ошибка входа';
  }
};

/**
 * Обработка регистрации
 * В текущей реализации не доступна (MVP)
 */
const handleRegister = async () => {
  errorMessage.value = '';

  if (
    !registerForm.value.username ||
    !registerForm.value.password ||
    !registerForm.value.passwordConfirm
  ) {
    errorMessage.value = 'Пожалуйста, заполните все поля';
    return;
  }

  if (registerForm.value.password !== registerForm.value.passwordConfirm) {
    errorMessage.value = 'Пароли не совпадают';
    return;
  }

  const success = await authStore.register(registerForm.value.username, registerForm.value.password);

  if (success) {
    router.push({ name: 'LandlordProperties' });
  } else {
    errorMessage.value = authStore.error || 'Ошибка регистрации';
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.auth-box {
  background-color: #fff;
  border-radius: 0.75rem;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.auth-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
  text-align: center;
}

.auth-subtitle {
  margin: 0 0 2rem 0;
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
}

.auth-form h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.9375rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  background-color: #667eea;
  color: #fff;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #5568d3;
}

.btn-primary:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-primary:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}

.form-hint {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
}

.link-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.link-btn:hover {
  color: #5568d3;
  text-decoration: underline;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fee;
  border-radius: 0.375rem;
  border-left: 4px solid #ef4444;
  color: #dc2626;
  font-size: 0.875rem;
}

.demo-credentials {
  margin-top: 1.5rem;
  padding: 0.875rem;
  background-color: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  color: #0369a1;
}

.demo-credentials .demo-title {
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.demo-credentials p {
  margin: 0.25rem 0;
}
</style>
