/**
 * Vue Router конфигурация
 * Маршруты приложения согласно архитектуре из PDF документации
 *
 * Структура маршрутов:
 * - /auth - аутентификация (логин/регистрация)
 * - /app - основное приложение с AppLayout (требует аутентификацию)
 *   - /app/landlord/* - функционал владельца (недвижимость, договоры, платежи, заявки, статистика)
 *   - /app/tenant/* - функционал арендатора (панель управления, договоры, платежи, заявки)
 *
 * Auth Flow:
 * 1. Неавторизованный пользователь → /auth/login
 * 2. После входа → восстановление сеанса из localStorage
 * 3. Попытка доступа к /app → проверка isAuthenticated
 * 4. Выход → очистка localStorage, редирект на /auth/login
 */

import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

// Layouts
import AppLayout from '../layouts/AppLayout.vue';
import LandlordLayout from '../layouts/LandlordLayout.vue';
import TenantLayout from '../layouts/TenantLayout.vue';
import AuthLayout from '../layouts/AuthLayout.vue';

// Pages - Auth
import LoginPage from '../../pages/auth/login.vue';

// Pages - Landlord
import LandlordPropertiesPage from '../../pages/landlord/properties.vue';
import LandlordContractsPage from '../../pages/landlord/contracts.vue';
import LandlordPaymentsPage from '../../pages/landlord/payments.vue';
import LandlordRequestsPage from '../../pages/landlord/requests.vue';
import LandlordStatisticsPage from '../../pages/landlord/statistics.vue';

// Pages - Tenant
import TenantDashboardPage from '../../pages/tenant/dashboard.vue';
import TenantContractPage from '../../pages/tenant/contract.vue';
import TenantPaymentsPage from '../../pages/tenant/payments.vue';
import TenantRequestsPage from '../../pages/tenant/requests.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/auth/login',
  },
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'AuthLogin',
        component: LoginPage,
        meta: { requiresAuth: false, title: 'Вход в систему' },
      },
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
            path: 'contracts',
            name: 'LandlordContracts',
            component: LandlordContractsPage,
            meta: { title: 'Договоры аренды' },
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
          {
            path: 'statistics',
            name: 'LandlordStatistics',
            component: LandlordStatisticsPage,
            meta: { title: 'Статистика' },
          },
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
            path: 'contracts',
            name: 'TenantContracts',
            component: TenantContractPage,
            meta: { title: 'Мои договоры' },
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
 *
 * Логика:
 * 1. Если маршрут требует аутентификацию (meta.requiresAuth = true)
 *    и пользователь не авторизован → редирект на /auth/login
 * 2. Если пользователь авторизован и пытается перейти на /auth/*
 *    → редирект на /app/landlord/properties
 * 3. Иначе → разрешить навигацию
 */
router.beforeEach((to) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth === true);

  if (requiresAuth && !authStore.isAuthenticated) {
    return '/auth/login';
  }

  if (authStore.isAuthenticated && to.path.startsWith('/auth')) {
    return '/app/landlord/properties';
  }

  return true;
});

export default router;
