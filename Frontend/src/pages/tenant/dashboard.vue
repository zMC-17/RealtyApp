<!-- pages/tenant/dashboard.vue -->
<template>
  <div class="content-page">
    <div class="content-inner">

      <header class="page-header">
        <div>
          <p class="page-eyebrow">Арендатор</p>
          <h1 class="page-title">Мой договор</h1>
        </div>
      </header>

      <!-- Лоадер -->
      <div v-if="tenantStore.loading" class="loader-wrap">
        <div class="loader-line"></div>
        <p class="loader-label">Загрузка данных…</p>
      </div>

      <!-- Ошибка -->
      <div v-else-if="tenantStore.error" class="empty-state">
        <div class="empty-icon-box">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.4"/>
            <path d="M10 6v5M10 13v1" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
        </div>
        <p class="empty-title">Ошибка загрузки</p>
        <p class="empty-text">{{ tenantStore.error }}</p>
        <button class="btn-ghost" @click="loadData">Попробовать снова</button>
      </div>

      <template v-else>

        <!-- Приглашение в договор -->
        <section v-if="tenantStore.hasPendingContracts" class="pending-section">
          <div class="pending-header">
            <span class="pending-pulse"></span>
            <h2 class="pending-title">Приглашение в договор</h2>
          </div>
          <p class="pending-desc">
            Владелец приглашает вас в договор аренды. Подтвердите участие или отклоните.
          </p>
          <div class="pending-list">
            <PendingContractCard
              v-for="contract in tenantStore.pendingContracts"
              :key="contract.id"
              :contract="contract"
              @confirm="handleConfirm"
            />
          </div>
        </section>

        <!-- Активный договор -->
        <section v-if="tenantStore.hasActiveContract" class="active-section">
          <h2 class="section-heading">Активный договор</h2>
          <ActiveContractCard :contract="tenantStore.activeContract!" />
          <QuickInfo :contract="tenantStore.activeContract!" />
        </section>

        <!-- Пусто -->
        <div v-if="!tenantStore.hasPendingContracts && !tenantStore.hasActiveContract" class="empty-state">
          <div class="empty-icon-box">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="2" width="14" height="16" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
              <path d="M7 7h6M7 11h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            </svg>
          </div>
          <p class="empty-title">Договоров пока нет</p>
          <p class="empty-text">Когда владелец добавит вас в договор аренды, он появится здесь</p>
        </div>

      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useTenantStore } from '../../stores/tenant';
import PendingContractCard from '../../components/tenant/PendingContractCard.vue';
import ActiveContractCard  from '../../components/tenant/ActiveContractCard.vue';
import QuickInfo           from '../../components/tenant/QuickInfo.vue';

const tenantStore = useTenantStore();
const loadData    = () => tenantStore.fetchContracts();
const handleConfirm = async (contractId: number) => {
  await tenantStore.confirmContract(contractId);
};
onMounted(loadData);
</script>

<style scoped>
.page-header {
  display: flex; align-items: flex-end; justify-content: space-between;
  margin-bottom: var(--space-8);
}
.page-eyebrow {
  font-size: var(--text-xs); font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--color-dark-35); margin-bottom: var(--space-1);
}
.page-title {
  font-size: var(--text-3xl); font-weight: 800; color: var(--color-dark);
  letter-spacing: -0.03em; line-height: 1;
}

/* ---- Лоадер ---- */
.loader-wrap {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--space-4); padding: var(--space-16);
}
.loader-line {
  width: 160px; height: 2px; background: rgba(28,26,23,0.10);
  border-radius: 1px; overflow: hidden; position: relative;
}
.loader-line::after {
  content: ''; position: absolute; inset: 0;
  background: var(--color-emerald);
  animation: loader 1.4s ease-in-out infinite;
}
@keyframes loader { 0% { transform: translateX(-100%); } 100% { transform: translateX(200%); } }
.loader-label { font-size: var(--text-sm); color: var(--color-dark-35); }

/* ---- Пустое состояние ---- */
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--space-3); padding: var(--space-16) var(--space-8); text-align: center;
}
.empty-icon-box {
  width: 52px; height: 52px; border-radius: var(--radius-lg);
  background: rgba(255,255,255,0.52); border: 1px solid rgba(255,255,255,0.65);
  backdrop-filter: blur(12px); display: flex; align-items: center; justify-content: center;
  margin-bottom: var(--space-2); color: var(--color-dark-35);
}
.empty-title { font-size: var(--text-lg); font-weight: 700; color: var(--color-dark); letter-spacing: -0.02em; }
.empty-text  { font-size: var(--text-sm); color: var(--color-dark-35); max-width: 300px; }
.btn-ghost {
  display: inline-flex; align-items: center; gap: var(--space-2);
  padding: var(--space-2) var(--space-4); margin-top: var(--space-2);
  background: rgba(255,255,255,0.50); border: 1px solid rgba(255,255,255,0.65);
  border-radius: var(--radius-md); color: var(--color-dark-60);
  font-family: var(--font-base); font-size: var(--text-sm);
  font-weight: 500; cursor: pointer; transition: all var(--transition);
  backdrop-filter: blur(8px);
}
.btn-ghost:hover { background: rgba(255,255,255,0.70); color: var(--color-dark); }

/* ---- Приглашение ---- */
.pending-section {
  background: rgba(255,255,255,0.42);
  backdrop-filter: blur(16px) saturate(130%);
  -webkit-backdrop-filter: blur(16px) saturate(130%);
  border: 1px solid rgba(255,255,255,0.60);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-6);
  box-shadow: 0 2px 0 rgba(255,255,255,0.65) inset, 0 8px 32px rgba(28,26,23,0.07);
  /* Левый акцент — тёплый персик, сигнализирует о действии */
  border-left: 3px solid var(--color-peach);
}

.pending-header {
  display: flex; align-items: center; gap: var(--space-3);
  margin-bottom: var(--space-2);
}

/* Пульсирующая точка — "требует внимания" */
.pending-pulse {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--color-peach); flex-shrink: 0;
  box-shadow: 0 0 0 3px rgba(196, 154, 120, 0.25);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(196, 154, 120, 0.25); }
  50%       { box-shadow: 0 0 0 6px rgba(196, 154, 120, 0.10); }
}

.pending-title {
  font-size: var(--text-md); font-weight: 700; color: var(--color-dark);
  letter-spacing: -0.02em;
}
.pending-desc {
  font-size: var(--text-sm); color: var(--color-dark-60);
  margin-bottom: var(--space-5); line-height: 1.55;
}
.pending-list { display: flex; flex-direction: column; gap: var(--space-3); }

/* ---- Активный договор ---- */
.active-section { margin-bottom: var(--space-8); }
.section-heading {
  font-size: var(--text-xs); font-weight: 700; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--color-dark-35);
  margin-bottom: var(--space-4);
}
</style>