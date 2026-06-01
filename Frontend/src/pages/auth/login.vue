<!-- pages/auth/login.vue -->
<template>
  <div class="login-page">
    <h2>Вход в систему</h2>

    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          placeholder="ivan@example.com"
        />
      </div>

      <div class="form-group">
        <label for="password">Пароль</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          placeholder="Минимум 8 символов"
        />
      </div>

      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>

      <button
        type="submit"
        :disabled="authStore.loading"
      >
        {{ authStore.loading ? 'Вход...' : 'Войти' }}
      </button>

      <p class="register-link">
        Нет аккаунта?
        <router-link to="/auth/register">Зарегистрироваться</router-link>
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');

const handleLogin = async () => {
  authStore.clearError();

  const success = await authStore.login({
    email: email.value,
    password: password.value,
  });

  if (success) {
    router.push({ name: 'LandlordProperties' });
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
