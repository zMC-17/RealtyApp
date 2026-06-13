<template>
  <div class="tenant-layout">
    <div class="layout-bg" aria-hidden="true">
      <div class="bg-base"></div>
      <div class="bg-blob bg-blob--rose"></div>
      <div class="bg-blob bg-blob--lilac"></div>
      <div class="bg-blob bg-blob--peach"></div>
      <div class="bg-blob bg-blob--olive"></div>
      <div class="bg-noise"></div>
    </div>

    <aside class="sidebar">
      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems" :key="item.name"
          :to="item.path" class="nav-item"
          :class="{ active: isActive(item.routeName) }"
        >
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="sidebar-footer-label">Арендатор</div>
      </div>
    </aside>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
const route    = useRoute();
const isActive = (routeName: string) => route.name === routeName;

const navItems = [
  {
    name: 'dashboard', routeName: 'TenantDashboard',
    path: '/app/tenant/dashboard', label: 'Мой договор',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <rect x="2" y="1" width="12" height="14" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
      <path d="M5 5h6M5 8h6M5 11h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`,
  },
  {
    name: 'payments', routeName: 'TenantPayments',
    path: '/app/tenant/payments', label: 'Платежи',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <rect x="1" y="4" width="14" height="9" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
      <path d="M1 7h14" stroke="currentColor" stroke-width="1.3"/>
      <circle cx="4.5" cy="10.5" r="1" fill="currentColor"/>
    </svg>`,
  },
  {
    name: 'requests', routeName: 'TenantRequests',
    path: '/app/tenant/requests', label: 'Заявки',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M13 2H3a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h3l2 2 2-2h3a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1Z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M5 6h6M5 9h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`,
  },
];
</script>

<style scoped>
.tenant-layout {
  position: relative;
  display: flex;
  width: 100%;
  height: 100%;
  overflow: hidden;
  isolation: isolate;
}

/* ---- Blob-фон: идентичен LandlordLayout ---- */
.layout-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.bg-base {
  position: absolute;
  inset: 0;
  background: #F2EDE3;
}

.bg-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(72px);
}

.bg-blob--rose {
  width: 65vw; height: 60vh;
  top: -18vh; right: -18vw;
  background: radial-gradient(
    circle at 40% 40%,
    rgba(196, 120, 138, 0.70) 0%,
    rgba(196, 120, 138, 0.32) 42%,
    transparent 68%
  );
}

.bg-blob--lilac {
  width: 60vw; height: 55vh;
  bottom: -14vh; left: -12vw;
  background: radial-gradient(
    circle at 60% 60%,
    rgba(155, 137, 180, 0.65) 0%,
    rgba(155, 137, 180, 0.28) 45%,
    transparent 68%
  );
}

.bg-blob--peach {
  width: 42vw; height: 38vh;
  bottom: -4vh; right: 8vw;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(196, 154, 120, 0.52) 0%,
    rgba(196, 154, 120, 0.18) 50%,
    transparent 70%
  );
}

.bg-blob--olive {
  width: 38vw; height: 32vh;
  top: 8vh; left: -4vw;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(141, 169, 138, 0.42) 0%,
    rgba(141, 169, 138, 0.15) 50%,
    transparent 70%
  );
}

.bg-noise {
  position: absolute;
  inset: 0;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size: 200px 200px;
}

/* ---- Стеклянный сайдбар ---- */
.sidebar {
  position: relative;
  z-index: 1;
  flex-shrink: 0;
  width: 196px;
  height: 100%;
  background: rgba(240, 238, 234, 0.55);
  backdrop-filter: blur(24px) saturate(140%);
  -webkit-backdrop-filter: blur(24px) saturate(140%);
  border-right: 1px solid rgba(255, 255, 255, 0.50);
  box-shadow: 1px 0 0 rgba(255, 255, 255, 0.30) inset, 4px 0 24px rgba(28, 26, 23, 0.04);
  display: flex;
  flex-direction: column;
  padding: var(--space-5) 0;
}

.sidebar-nav {
  display: flex; flex-direction: column;
  gap: 2px; padding: 0 var(--space-3); flex: 1;
}

.nav-item {
  position: relative;
  display: flex; align-items: center;
  gap: var(--space-3); padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md); text-decoration: none;
  color: var(--color-dark-60); font-size: var(--text-sm);
  font-weight: 500; transition: all var(--transition);
}
.nav-item:hover { background: rgba(255, 255, 255, 0.40); color: var(--color-dark); }
.nav-item.active { background: rgba(26, 107, 74, 0.10); color: var(--color-emerald); font-weight: 600; }
.nav-item.active::before {
  content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%);
  width: 3px; height: 20px; background: var(--color-emerald); border-radius: 0 2px 2px 0;
}
.nav-icon { flex-shrink: 0; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; }
.nav-label { white-space: nowrap; }

.sidebar-footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid rgba(28, 26, 23, 0.08);
  margin-top: var(--space-3);
}
.sidebar-footer-label {
  font-size: var(--text-xs); font-weight: 700;
  letter-spacing: 0.09em; text-transform: uppercase; color: var(--color-dark-35);
}

/* ---- Контент прозрачный ---- */
.content {
  position: relative; z-index: 1;
  flex: 1; overflow-y: auto; overflow-x: hidden; min-width: 0;
}
</style>