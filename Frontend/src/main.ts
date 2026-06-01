import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

import PrimeVue from 'primevue/config';
import './style.css';
import router from './router/index.ts';
import { useAuthStore } from './stores/auth';

const app = createApp(App);
// Подключаем Pinia хранилище

const pinia = createPinia();
app.use(pinia);

// Подключаем PrimeVue
app.use(PrimeVue);

// Подключаем Vue Router
app.use(router);

// Монтируем приложение
app.mount('#app');
