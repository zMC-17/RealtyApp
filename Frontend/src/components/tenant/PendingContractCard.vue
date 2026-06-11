<!-- components/tenant/PendingContractCard.vue -->
<template>
  <div class="pending-card">
    <div class="card-body">

      <div class="info-grid">
        <div class="info-block">
          <span class="info-label">Объект</span>
          <span class="info-value">{{ contract.property_info?.title || '—' }}</span>
          <span class="info-sub">{{ contract.property_info?.address }}</span>
        </div>
        <div class="info-block">
          <span class="info-label">Владелец</span>
          <span class="info-value">{{ contract.owner_info?.name || '—' }}</span>
          <span class="info-sub">{{ contract.owner_info?.email }}</span>
        </div>
      </div>

      <div class="meta-row">
        <div class="meta-item">
          <span class="info-label">Период</span>
          <span class="info-value">{{ formatDate(contract.start_date) }} — {{ formatDate(contract.end_date) }}</span>
        </div>
        <div class="meta-item">
          <span class="info-label">Платёж / мес</span>
          <span class="info-value info-value--amount">{{ formatCurrency(contract.monthly_payment) }}</span>
        </div>
        <div class="meta-item">
          <span class="info-label">Депозит</span>
          <span class="info-value">{{ formatCurrency(contract.security_deposit) }}</span>
        </div>
      </div>

    </div>

    <div class="card-footer">
      <button class="btn-confirm" @click="$emit('confirm', contract.id)">
        Принять договор
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ContractWithDetails } from '../../types/contract';
defineProps<{ contract: ContractWithDetails }>();
defineEmits<{ confirm: [contractId: number] }>();
const formatDate     = (d: string) => new Date(d).toLocaleDateString('ru-RU');
const formatCurrency = (v: string) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(parseFloat(v));
</script>

<style scoped>
.pending-card {
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(16px) saturate(130%);
  -webkit-backdrop-filter: blur(16px) saturate(130%);
  border: 1px solid rgba(255,255,255,0.70);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 2px 0 rgba(255,255,255,0.70) inset, 0 4px 20px rgba(28,26,23,0.06);
}

.card-body {
  padding: var(--space-5);
  display: flex; flex-direction: column; gap: var(--space-4);
}

.info-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4);
}

.info-block {
  display: flex; flex-direction: column; gap: 2px;
}

.meta-row {
  display: flex; gap: var(--space-6); flex-wrap: wrap;
  padding-top: var(--space-4);
  border-top: 1px solid rgba(28,26,23,0.08);
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

.card-footer {
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid rgba(28,26,23,0.08);
  background: rgba(26,107,74,0.04);
}

.btn-confirm {
  width: 100%; padding: var(--space-3);
  background: var(--color-emerald); color: #fff;
  border: none; border-radius: var(--radius-md);
  font-family: var(--font-base); font-size: var(--text-sm);
  font-weight: 700; cursor: pointer; transition: all var(--transition);
  letter-spacing: -0.01em;
}
.btn-confirm:hover {
  background: #155c3e;
  box-shadow: 0 4px 16px rgba(26,107,74,0.30);
  transform: translateY(-1px);
}
.btn-confirm:active { transform: translateY(0); }
</style>