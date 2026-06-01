<template>
  <div class="app-container">
    <!-- Заголовок с переключателем ролей -->
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">RealtyApp</h1>

        <!-- Переключатель режимов работы (Владелец / Арендатор) -->
        <div class="role-selector">
          <button class="role-btn" :class="{ active: roleStore.getRole === 'landlord' }"
            @click="switchRole('landlord')">
            Владелец
          </button>
          <button class="role-btn" :class="{ active: roleStore.getRole === 'tenant' }" @click="switchRole('tenant')">
            Арендатор
          </button>
        </div>

        <!-- Кнопка выхода -->
        <button class="logout-btn" @click="logout">
          Выход
        </button>
      </div>
    </header>

    <!-- Основная область содержимого -->
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">

import { useRouter } from 'vue-router';
import type { UserRole } from '../types';
import { onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
import { useRoleStore } from '../stores/role';
import { useAuthStore } from '../stores/auth';
const roleStore = useRoleStore();
const authStore = useAuthStore();


const syncRoleFromUrl = () => {
  if (route.path.includes('/tenant')) {
    roleStore.setRole('tenant');
  } else if (route.path.includes('/landlord')) {
    roleStore.setRole('landlord');
  }
};

// Запускаем при монтировании компонента
onMounted(syncRoleFromUrl);

// И при каждом изменении маршрута
watch(() => route.path, syncRoleFromUrl);
/**
 * Переключение между ролями владельца и арендатора
 * При смене роли перенаправляет на первую страницу соответствующего раздела
 */
const switchRole = (role: UserRole) => {
  roleStore.setRole(role);

  if (role === 'landlord') {
    router.push({ name: 'LandlordProperties' });
  } else {
    router.push({ name: 'TenantDashboard' });
  }
};

/*
 * Выход из системы
 */
const logout = () => {
  // TODO: Интеграция с хранилищем и очистка токена
  authStore.logout();
  router.push({ name: 'AuthLogin' });
};
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
}

.app-header {
  flex-shrink: 0;
  width: 100%;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.app-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.role-selector {
  display: flex;
  gap: 0.5rem;
  background-color: #f0f0f0;
  padding: 0.25rem;
  border-radius: 0.375rem;
}

.role-btn {
  padding: 0.5rem 1rem;
  border: none;
  background-color: transparent;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s ease;
}

.role-btn:hover {
  color: #374151;
}

.role-btn.active {
  background-color: #fff;
  color: #1f2937;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.logout-btn {
  padding: 0.5rem 1rem;
  background-color: transparent;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  color: #6b7280;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  border-color: #9ca3af;
  color: #374151;
}

.app-main {
  flex: 1;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Скроллинг для очень длинного содержимого */
.app-main::-webkit-scrollbar {
  width: 8px;
}

.app-main::-webkit-scrollbar-track {
  background: transparent;
}

.app-main::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

.app-main::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>