<!-- components/tenant/ActiveContractCard.vue -->
<template>
  <div class="active-card">

    <!-- Шапка с изумрудным акцентом -->
    <div class="card-header">
      <div class="header-left">
        <span class="status-dot"></span>
        <span class="status-label">Договор активен</span>
      </div>
      <span class="contract-id">#{{ contract.id }}</span>
    </div>

    <div class="card-body">

      <div class="info-grid">
        <div class="info-block">
          <span class="info-label">Объект</span>
          <span class="info-value">{{ contract.property_info?.title }}</span>
          <span class="info-sub">{{ contract.property_info?.address }}</span>
        </div>
        <div class="info-block">
          <span class="info-label">Владелец</span>
          <span class="info-value">{{ contract.owner_info?.name }}</span>
          <span class="info-sub">{{ contract.owner_info?.email }}</span>
        </div>
      </div>

      <div class="meta-row">
        <div class="meta-item">
          <span class="info-label">Период</span>
          <span class="info-value">{{ formatDate(contract.start_date) }} — {{ formatDate(contract.end_date) }}</span>
        </div>
        <div class="meta-item">
          <span class="info-label">Ежемесячный платёж</span>
          <span class="info-value info-value--amount">{{ formatCurrency(contract.monthly_payment) }}</span>
        </div>
        <div v-if="contract.security_deposit" class="meta-item">
          <span class="info-label">Депозит</span>
          <span class="info-value">{{ formatCurrency(contract.security_deposit) }}</span>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import type { ContractWithDetails } from '../../types/contract';
defineProps<{ contract: ContractWithDetails }>();
const formatDate     = (d: string) => new Date(d).toLocaleDateString('ru-RU');
const formatCurrency = (v: string) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(parseFloat(v));
</script>

<style scoped>
.active-card {
  background: rgba(255,255,255,0.52);
  backdrop-filter: blur(20px) saturate(140%);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  border: 1px solid rgba(255,255,255,0.65);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: var(--space-4);
  box-shadow: 0 2px 0 rgba(255,255,255,0.70) inset, 0 8px 32px rgba(28,26,23,0.08);
}

/* Тонкая изумрудная полоска сверху */
.active-card::before {
  content: '';
  display: block;
  height: 3px;
  background: linear-gradient(90deg, var(--color-emerald), var(--color-olive));
}

.card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid rgba(28,26,23,0.08);
}

.header-left { display: flex; align-items: center; gap: var(--space-2); }

.status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--color-emerald); flex-shrink: 0;
  box-shadow: 0 0 0 3px var(--color-emerald-20);
}

.status-label {
  font-size: var(--text-xs); font-weight: 700;
  letter-spacing: 0.07em; text-transform: uppercase; color: var(--color-emerald);
}

.contract-id {
  font-size: var(--text-xs); font-weight: 600;
  color: var(--color-dark-35); font-variant-numeric: tabular-nums;
}

.card-body {
  padding: var(--space-5); display: flex; flex-direction: column; gap: var(--space-4);
}

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); }
.info-block { display: flex; flex-direction: column; gap: 2px; }

.meta-row {
  display: flex; gap: var(--space-6); flex-wrap: wrap;
  padding-top: var(--space-4); border-top: 1px solid rgba(28,26,23,0.08);
}
.meta-item { display: flex; flex-direction: column; gap: 2px; }

.info-label {
  font-size: var(--text-xs); font-weight: 600;
  letter-spacing: 0.06em; text-transform: uppercase; color: var(--color-dark-35);
}
.info-value { font-size: var(--text-sm); font-weight: 600; color: var(--color-dark); }
.info-value--amount {
  font-size: var(--text-md); font-weight: 800;
  color: var(--color-emerald); letter-spacing: -0.02em; font-variant-numeric: tabular-nums;
}
.info-sub { font-size: var(--text-xs); color: var(--color-dark-35); }
</style>