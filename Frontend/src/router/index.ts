/**
 * Vue Router конфигурация
 * Маршруты приложения
 */

import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/auth.ts';

// Layouts
import AppLayout from '../layouts/AppLayout.vue';
import LandlordLayout from '../layouts/LandlordLayout.vue';
import TenantLayout from '../layouts/TenantLayout.vue';
import AuthLayout from '../layouts/AuthLayout.vue';

// Pages - Auth
import LoginPage from '../pages/auth/login.vue';
import RegisterPage from '../pages/auth/register.vue'

// Pages - Landlord
import LandlordPropertiesPage from '../pages/landlord/properties.vue';
import LandlordPaymentsPage from '../pages/landlord/payments.vue';
import LandlordRequestsPage from '../pages/landlord/requests.vue';
import LandlordStatisticsPage from '../pages/landlord/statistics.vue';

// Pages - Tenant
import TenantDashboardPage from '../pages/tenant/dashboard.vue';
import TenantPaymentsPage from '../pages/tenant/payments.vue';
import TenantRequestsPage from '../pages/tenant/requests.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/auth/login',
  },
  {
    path: '/auth',
    component: AuthLayout,
    meta: { requiresGuest: true },
    children: [
      {
        path: 'login',
        name: 'AuthLogin',
        component: LoginPage,
        meta: { requiresAuth: false, title: 'Вход в систему' },
      },
      {
        path: 'register',
        name: 'AuthRegister',
        component: RegisterPage,
        meta: { requiresAuth: false, title: 'Регистрация' }
      }
    ],
  },
  {
    path: '/app',
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      // Маршруты владельца (Landlord)
      {
        path: 'landlord',
        component: LandlordLayout,
        children: [
          {
            path: 'properties',
            name: 'LandlordProperties',
            component: LandlordPropertiesPage,
            meta: { title: 'Мои объекты' },
          },
          {
            path: 'properties/:id',
            name: 'PropertyDetail',
            component: () => import('../pages/landlord/property-detail.vue'),
            meta: { title: 'Детали объекта' },
          },
          {
            path: 'payments',
            name: 'LandlordPayments',
            component: LandlordPaymentsPage,
            meta: { title: 'Платежи' },
          },
          {
            path: 'requests',
            name: 'LandlordRequests',
            component: LandlordRequestsPage,
            meta: { title: 'Заявки от арендаторов' },
          },
          // {
          //   path: 'statistics',
          //   name: 'LandlordStatistics',
          //   component: LandlordStatisticsPage,
          //   meta: { title: 'Статистика' },
          // },
        ],
      },

      // Маршруты арендатора (Tenant)
      {
        path: 'tenant',
        component: TenantLayout,
        children: [
          {
            path: 'dashboard',
            name: 'TenantDashboard',
            component: TenantDashboardPage,
            meta: { title: 'Панель управления' },
          },
          {
            path: 'payments',
            name: 'TenantPayments',
            component: TenantPaymentsPage,
            meta: { title: 'Платежи' },
          },
          {
            path: 'requests',
            name: 'TenantRequests',
            component: TenantRequestsPage,
            meta: { title: 'Мои заявки' },
          },
        ],
      },

      // Редирект при попадании в /app без подпути
      {
        path: '',
        redirect: 'landlord/properties',
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/auth/login',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

/**
 * Router Guard: Проверка аутентификации перед навигацией
 */
router.beforeEach(async (to) => {
  const authStore = useAuthStore();

  // 1. Восстанавливаем сессию при перезагрузке
  if (!authStore.isAuthenticated && localStorage.getItem('access_token')) {
    await authStore.checkAuth();
  }

  // 2. Проверяем вложенные маршруты
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth === true);
  const requiresGuest = to.matched.some(record => record.meta.requiresGuest === true);

  // 3. Защищённый маршрут, но не авторизован
  if (requiresAuth && !authStore.isAuthenticated) {
    return { name: 'AuthLogin', query: { redirect: to.fullPath } };
  }

  // 4. Гостевой маршрут, но уже авторизован
  if (requiresGuest && authStore.isAuthenticated) {
    return { name: 'LandlordProperties' };
  }

  // 5. Публичный маршрут
  return true;
});

export default router;
