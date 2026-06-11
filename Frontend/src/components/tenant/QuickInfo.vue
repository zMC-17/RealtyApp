<!-- components/tenant/QuickInfo.vue -->
<template>
  <div class="quick-info">

    <div class="quick-card">
      <div class="quick-icon-wrap">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <rect x="1" y="3" width="14" height="12" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
          <path d="M1 7h14M5 1v4M11 1v4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="quick-text">
        <span class="quick-label">Следующий платёж</span>
        <span class="quick-value">{{ nextPaymentDate }}</span>
      </div>
    </div>

    <div class="quick-card">
      <div class="quick-icon-wrap">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.3"/>
          <path d="M8 4.5v4l2.5 1.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="quick-text">
        <span class="quick-label">Осталось месяцев</span>
        <span class="quick-value quick-value--large">{{ remainingMonths }}</span>
      </div>
    </div>

    <div class="quick-card quick-card--accent">
      <div class="quick-icon-wrap quick-icon-wrap--emerald">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <rect x="1" y="4" width="14" height="9" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
          <path d="M1 7h14" stroke="currentColor" stroke-width="1.3"/>
          <circle cx="4.5" cy="10.5" r="1" fill="currentColor"/>
        </svg>
      </div>
      <div class="quick-text">
        <span class="quick-label">Ежемесячный платёж</span>
        <span class="quick-value quick-value--currency">{{ formatCurrency(contract.monthly_payment) }}</span>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ContractWithDetails } from '../../types/contract';

const props = defineProps<{ contract: ContractWithDetails }>();

const nextPaymentDate = computed(() => {
  const now = new Date();
  const day = new Date(props.contract.start_date).getDate();
  const next = new Date(now.getFullYear(), now.getMonth(), day);
  if (next <= now) next.setMonth(next.getMonth() + 1);
  return next.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
});

const remainingMonths = computed(() => {
  const now = new Date();
  const end = new Date(props.contract.end_date);
  return Math.max(0, (end.getFullYear() - now.getFullYear()) * 12 + (end.getMonth() - now.getMonth()));
});

const formatCurrency = (v: string) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(parseFloat(v));
</script>

<style scoped>
.quick-info {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}
@media (max-width: 700px) {
  .quick-info { grid-template-columns: 1fr; }
}

.quick-card {
  background: rgba(255,255,255,0.52);
  backdrop-filter: blur(20px) saturate(140%);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  border: 1px solid rgba(255,255,255,0.65);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  display: flex; align-items: flex-start; gap: var(--space-3);
  box-shadow: 0 2px 0 rgba(255,255,255,0.70) inset, 0 4px 16px rgba(28,26,23,0.06);
  transition: box-shadow var(--transition), border-color var(--transition);
}
.quick-card:hover {
  box-shadow: 0 2px 0 rgba(255,255,255,0.80) inset, 0 8px 28px rgba(28,26,23,0.09);
}

/* Акцентная карточка с изумрудной верхней полосой */
.quick-card--accent { position: relative; overflow: hidden; }
.quick-card--accent::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0;
  height: 2px; background: linear-gradient(90deg, var(--color-emerald), var(--color-olive));
}

.quick-icon-wrap {
  flex-shrink: 0;
  width: 32px; height: 32px;
  border-radius: var(--radius-md);
  background: rgba(28,26,23,0.06);
  display: flex; align-items: center; justify-content: center;
  color: var(--color-dark-60);
}
.quick-icon-wrap--emerald {
  background: var(--color-emerald-08);
  color: var(--color-emerald);
}

.quick-text { display: flex; flex-direction: column; gap: var(--space-1); }

.quick-label {
  font-size: var(--text-xs); font-weight: 600;
  letter-spacing: 0.06em; text-transform: uppercase; color: var(--color-dark-35);
}

.quick-value {
  font-size: var(--text-base); font-weight: 700; color: var(--color-dark);
  font-variant-numeric: tabular-nums;
}
.quick-value--large {
  font-size: var(--text-2xl); font-weight: 800;
  letter-spacing: -0.03em; line-height: 1;
}
.quick-value--currency {
  font-size: var(--text-xl); font-weight: 800;
  color: var(--color-emerald); letter-spacing: -0.03em; line-height: 1;
}
</style>