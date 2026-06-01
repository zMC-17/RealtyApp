<template>
  <div class="tenant-layout">
    <!-- Верхняя навигационная панель -->
    <nav class="nav-bar">

      <!-- Кнопка дашборда -->
      <router-link
        to="/app/tenant/dashboard"
        class="nav-tab"
        :class="{ active: isActive('TenantDashboard') }"
      >
        <span class="nav-icon">📊</span>
        <span class="nav-label">Панель управления</span>
      </router-link>
      <!-- Кнопка платежей -->
      <router-link
        to="/app/tenant/payments"
        class="nav-tab"
        :class="{ active: isActive('TenantPayments') }"
      >
        <span class="nav-icon">💳</span>
        <span class="nav-label">Платежи</span>
      </router-link>
      <!-- Кнопка заявок -->
      <router-link
        to="/app/tenant/requests"
        class="nav-tab"
        :class="{ active: isActive('TenantRequests') }"
      >
        <span class="nav-icon">🔧</span>
        <span class="nav-label">Заявки</span>
      </router-link>
    </nav>

    <!-- Основная область содержимого -->
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
/**
 * TenantLayout - Вложенный layout для функционала арендатора
 *
 * Отображает боковую панель с кнопками разделов:
 * - Договоры
 * - Платежи
 * - Заявки
 */

import { useRoute } from 'vue-router';

const route = useRoute();

/**
 * Проверить активный ли маршрут
 */
const isActive = (routeName: string) => route.name === routeName;
</script>

<style scoped>
.tenant-layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.nav-bar {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0;
  width: 100%;
  background-color: #fff;
  border-bottom: 2px solid #e5e7eb;
  padding: 0;
  overflow-x: auto;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.nav-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1.25rem 1.5rem;
  color: #6b7280;
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 500;
  white-space: nowrap;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  position: relative;
  margin-bottom: -2px;
}

.nav-tab:hover {
  background-color: #f9fafb;
  color: #374151;
}

.nav-tab.active {
  background-color: #f0f4ff;
  color: #667eea;
  border-bottom-color: #667eea;
}

.nav-icon {
  font-size: 1.25rem;
  width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-label {
  font-size: 0.95rem;
}

.content {
  flex: 1;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Скроллинг для длинного содержимого */
.content::-webkit-scrollbar {
  width: 8px;
}

.content::-webkit-scrollbar-track {
  background: transparent;
}

.content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

.content::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
