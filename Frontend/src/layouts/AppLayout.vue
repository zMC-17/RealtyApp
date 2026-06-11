<template>
  <div class="app-container">

    <!-- Стеклянный хедер — фон просвечивает из дочернего лейаута -->
    <header class="app-header">
      <div class="header-inner">
        <div class="app-brand">
          <span class="brand-mark">R</span>
          <span class="brand-name">Realty</span>
        </div>

        <div class="role-switcher">
          <button class="role-btn" :class="{ active: roleStore.getRole === 'landlord' }"
            @click="switchRole('landlord')">
            Владелец
          </button>
          <button class="role-btn" :class="{ active: roleStore.getRole === 'tenant' }" @click="switchRole('tenant')">
            Арендатор
          </button>
        </div>

        <button class="logout-btn" @click="logout">
          <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
            <path d="M6 2H2.5a.5.5 0 0 0-.5.5v10a.5.5 0 0 0 .5.5H6M10 10.5l3-3-3-3M13 7.5H5.5" stroke="currentColor"
              stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          Выход
        </button>
      </div>
    </header>

    <main class="app-main">
      <router-view />
    </main>

  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import type { UserRole } from '../types';
import { onMounted, watch } from 'vue';
import { useRoleStore } from '../stores/role';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const route = useRoute();
const roleStore = useRoleStore();
const authStore = useAuthStore();

const syncRoleFromUrl = () => {
  if (route.path.includes('/tenant')) roleStore.setRole('tenant');
  else if (route.path.includes('/landlord')) roleStore.setRole('landlord');
};

onMounted(syncRoleFromUrl);
watch(() => route.path, syncRoleFromUrl);

const switchRole = (role: UserRole) => {
  roleStore.setRole(role);
  router.push({ name: role === 'landlord' ? 'LandlordDashboard' : 'TenantDashboard' });
};

const logout = () => {
  authStore.logout();
  router.push({ name: 'AuthLogin' });
};
</script>

<style scoped>
/* Контейнер — прозрачный, фон идёт из дочернего лейаута (Landlord/Tenant) */
.app-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: transparent;
}

/* ---- Стеклянный хедер ---- */
/*
  Лежит поверх blob-фона дочернего лейаута.
  Стекло чуть плотнее, чем сайдбар — он «ближе» к пользователю.
*/
.app-header {
  position: relative;
  z-index: 10;
  flex-shrink: 0;
  width: 100%;
  height: 56px;
  padding: 0 var(--space-8);
  /* Стекло */
  background: rgba(242, 237, 227, 0.60);
  backdrop-filter: blur(20px) saturate(150%);
  -webkit-backdrop-filter: blur(20px) saturate(150%);
  /* Нижняя граница — полупрозрачная, не режет фон */
  border-bottom: 1px solid rgba(255, 255, 255, 0.45);
  /* Блик снизу имитирует толщину стекла */
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.35) inset,
    0 1px 12px rgba(28, 26, 23, 0.06);
}

.header-inner {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  height: 100%;
}

/* ---- Бренд ---- */
.app-brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-right: auto;
  flex-shrink: 0;
}

.brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: var(--color-emerald);
  color: #fff;
  font-family: var(--font-base);
  font-size: var(--text-sm);
  font-weight: 800;
  letter-spacing: -0.02em;
  border-radius: var(--radius-sm);
}

.brand-name {
  font-family: var(--font-base);
  font-size: var(--text-md);
  font-weight: 700;
  color: var(--color-dark);
  letter-spacing: -0.02em;
}

/* ---- Переключатель ролей ---- */
.role-switcher {
  display: flex;
  align-items: center;
  gap: 2px;
  background: rgba(28, 26, 23, 0.08);
  padding: 3px;
  border-radius: var(--radius-md);
}

.role-btn {
  padding: var(--space-2) var(--space-4);
  border: none;
  background: transparent;
  border-radius: 5px;
  cursor: pointer;
  font-family: var(--font-base);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-dark-60);
  transition: all var(--transition);
  white-space: nowrap;
}

.role-btn:hover {
  color: var(--color-dark);
}

.role-btn.active {
  background: var(--color-dark);
  color: var(--color-bg);
  font-weight: 600;
}

/* ---- Выход ---- */
.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: transparent;
  border: 1px solid rgba(28, 26, 23, 0.12);
  border-radius: var(--radius-md);
  color: var(--color-dark-60);
  cursor: pointer;
  font-family: var(--font-base);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: all var(--transition);
  flex-shrink: 0;
}

.logout-btn:hover {
  border-color: rgba(28, 26, 23, 0.25);
  color: var(--color-dark);
  background: rgba(255, 255, 255, 0.35);
}

/* ---- Main ---- */
.app-main {
  flex: 1;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  /* Прозрачный — дочерний лейаут несёт фон */
  background: transparent;
}
</style>