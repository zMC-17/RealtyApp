import { createApp } from 'vue';
import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';
import './style.css';
import App from './App.vue';
import router from './app/router';
import { useAuthStore } from './stores/auth';

/**
 * Инициализация приложения RealtyApp
 *
 * Порядок подключения:
 * 1. Создание приложения Vue
 * 2. Подключение Pinia для управления состоянием
 * 3. Инициализация auth store (восстановление сеанса из localStorage)
 * 4. Подключение PrimeVue
 * 5. Подключение Vue Router
 * 6. Монтирование в DOM
 */

const app = createApp(App);

// Подключаем Pinia хранилище
const pinia = createPinia();
app.use(pinia);

// Инициализируем auth store для восстановления сеанса
// ВАЖНО: должно быть после app.use(pinia)
const authStore = useAuthStore();
authStore.initializeAuth();

// Подключаем PrimeVue (обязательно для Dialog, Tag, Button и других компонентов)
app.use(PrimeVue);

// Подключаем Vue Router
app.use(router);

// Монтируем приложение
app.mount('#app');
