<!-- pages/auth/login.vue -->
<template>
  <div class="auth-card">

    <div class="auth-head">
      <h1 class="auth-title">Добро пожаловать</h1>
      <p class="auth-sub">Войдите, чтобы продолжить</p>
    </div>

    <form @submit.prevent="handleLogin" class="auth-form">
      <div class="field">
        <label class="field-label" for="email">Email</label>
        <input class="field-input" id="email" v-model="email" type="email" required placeholder="ivan@example.com"
          autocomplete="email" />
      </div>

      <div class="field">
        <label class="field-label" for="password">Пароль</label>
        <input class="field-input" id="password" v-model="password" type="password" required placeholder="••••••••"
          autocomplete="current-password" />
      </div>

      <div v-if="authStore.error" class="auth-error">
        {{ authStore.error }}
      </div>

      <button class="auth-submit" type="submit" :disabled="authStore.loading">
        <span v-if="authStore.loading" class="submit-spinner"></span>
        {{ authStore.loading ? 'Входим…' : 'Войти' }}
      </button>
    </form>

    <p class="auth-footer-link">
      Нет аккаунта?
      <router-link to="/auth/register">Зарегистрироваться</router-link>
    </p>

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
  const success = await authStore.login({ email: email.value, password: password.value });
  if (success) router.push({ name: 'LandlordDashboard' });
};
</script>

<style scoped>
/* ============ Карточка ============ */
/*
  Намеренно НЕ на весь экран.
  Стекло — работает поверх насыщенного градиента в AuthLayout.
*/
.auth-card {
  background: rgba(255, 255, 255, 0.62);
  backdrop-filter: blur(32px) saturate(160%);
  -webkit-backdrop-filter: blur(32px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.75);
  border-radius: var(--radius-xl);
  padding: var(--space-10) var(--space-8);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  /* Лёгкая внутренняя тень — карточка «лежит» на фоне, а не висит */
  box-shadow:
    0 2px 0 rgba(255, 255, 255, 0.8) inset,
    0 16px 48px rgba(28, 26, 23, 0.14),
    0 4px 12px rgba(28, 26, 23, 0.08);
}

/* ============ Заголовок ============ */
.auth-head {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.auth-title {
  font-size: var(--text-2xl);
  font-weight: 800;
  color: var(--color-dark);
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.auth-sub {
  font-size: var(--text-sm);
  color: var(--color-dark-35);
  font-weight: 500;
}

/* ============ Форма ============ */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

/* Поля чуть светлее фона карточки — они «утоплены» */
.field-input {
  padding: var(--space-3) var(--space-4);
  background: rgba(255, 255, 255, 0.70);
  border: 1px solid rgba(28, 26, 23, 0.12);
  border-radius: var(--radius-md);
  color: var(--color-dark);
  font-family: var(--font-base);
  font-size: var(--text-base);
  transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
  width: 100%;
}

.field-input::placeholder {
  color: var(--color-dark-35);
}

.field-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.90);
  border-color: var(--color-emerald-20);
  box-shadow: 0 0 0 3px var(--color-emerald-08);
}

/* ============ Кнопка ============ */
.auth-submit {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--color-dark);
  color: var(--color-bg);
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-base);
  font-size: var(--text-base);
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  margin-top: var(--space-2);
  letter-spacing: -0.01em;
}

.auth-submit:hover:not(:disabled) {
  background: #2d2b27;
  box-shadow: 0 4px 16px rgba(28, 26, 23, 0.20);
  transform: translateY(-1px);
}

.auth-submit:active:not(:disabled) {
  transform: translateY(0);
}

.auth-submit:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.submit-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.30);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
  flex-shrink: 0;
}

/* ============ Ошибка ============ */
.auth-error {
  padding: var(--space-3) var(--space-4);
  background: var(--color-danger-bg);
  border: 1px solid rgba(185, 64, 64, 0.20);
  border-radius: var(--radius-md);
  color: var(--color-danger);
  font-size: var(--text-sm);
  font-weight: 500;
}

/* ============ Ссылка ============ */
.auth-footer-link {
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-dark-35);
  font-weight: 500;
}

.auth-footer-link a {
  color: var(--color-emerald);
  font-weight: 700;
  text-decoration: none;
  transition: opacity var(--transition);
}

.auth-footer-link a:hover {
  opacity: 0.75;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>