<!-- pages/auth/register.vue -->
<template>
  <div class="register-page">
    <h2>Регистрация</h2>

    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="name">Имя</label>
        <input
          id="name"
          v-model="name"
          type="text"
          required
          placeholder="Иван Петров"
          minlength="2"
          maxlength="50"
        />
      </div>

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
          minlength="8"
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Подтверждение пароля</label>
        <input
          id="confirmPassword"
          v-model="confirmPassword"
          type="password"
          required
          placeholder="Повторите пароль"
        />
        <span v-if="passwordMismatch" class="validation-error">
          Пароли не совпадают
        </span>
      </div>

      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>

      <button
        type="submit"
        :disabled="authStore.loading || passwordMismatch"
      >
        {{ authStore.loading ? 'Регистрация...' : 'Зарегистрироваться' }}
      </button>

      <p class="login-link">
        Уже есть аккаунт?
        <router-link to="/auth/login">Войти</router-link>
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

// Проверка совпадения паролей
const passwordMismatch = computed(() => {
  return confirmPassword.value.length > 0 && password.value !== confirmPassword.value;
});

const handleRegister = async () => {
  // Дополнительная проверка перед отправкой
  if (password.value !== confirmPassword.value) {
    return;
  }

  authStore.clearError();

  const success = await authStore.register({
    name: name.value,
    email: email.value,
    password: password.value,
  });

  if (success) {
    // После успешной регистрации перенаправляем на главную
    router.push({ name: 'LandlordProperties' });
  }
};
</script>

<style scoped>
.register-page {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.validation-error {
  display: block;
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.error-message {
  background: #fee;
  color: #c0392b;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

button {
  width: 100%;
  padding: 0.875rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover:not(:disabled) {
  background: #5a6fd6;
}

button:disabled {
  background: #b3b3b3;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>