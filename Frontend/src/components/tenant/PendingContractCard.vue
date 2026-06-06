<!-- components/tenant/PendingContractCard.vue -->
<template>
    <div class="pending-card">
        <div class="pending-card__body">
            <div class="info-row">
                <span class="info-icon">🏠</span>
                <div>
                    <span class="info-label">Объект</span>
                    <strong>{{ contract.property_info?.title || '—' }}</strong>
                    <p class="info-sub">{{ contract.property_info?.address }}</p>
                </div>
            </div>

            <div class="info-row">
                <span class="info-icon">👤</span>
                <div>
                    <span class="info-label">Владелец</span>
                    <strong>{{ contract.owner_info?.name || '—' }}</strong>
                    <p class="info-sub">{{ contract.owner_info?.email }}</p>
                </div>
            </div>

            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Период</span>
                    <strong>{{ formatDate(contract.start_date) }} — {{ formatDate(contract.end_date) }}</strong>
                </div>
                <div class="info-item">
                    <span class="info-label">Ежемесячный платёж</span>
                    <strong class="amount">{{ formatCurrency(contract.monthly_payment) }}</strong>
                </div>
                <div class="info-item">
                    <span class="info-label">Депозит</span>
                    <strong>{{ formatCurrency(contract.security_deposit) }}</strong>
                </div>
            </div>
        </div>

        <div class="pending-card__actions">
            <button class="btn-confirm" @click="$emit('confirm', contract.id)">
                ✅ Принять договор
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { ContractWithDetails } from '../../types/contract';

defineProps<{ contract: ContractWithDetails }>();
defineEmits<{ confirm: [contractId: number] }>();

const formatDate = (d: string) => new Date(d).toLocaleDateString('ru-RU');
const formatCurrency = (v: string) =>
    new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(parseFloat(v));
</script>

<style scoped>
.pending-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.pending-card__body {
    padding: 1.5rem;
}

.info-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.info-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.info-label {
    display: block;
    font-size: 0.75rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.info-sub {
    margin: 0.125rem 0 0 0;
    color: #6b7280;
    font-size: 0.875rem;
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}

.amount {
    color: #059669;
}

.pending-card__actions {
    padding: 1rem 1.5rem;
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
    display: flex;
    gap: 0.75rem;
}

.btn-confirm {
    flex: 1;
    padding: 0.75rem;
    background: #10b981;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-confirm:hover {
    background: #059669;
}
</style>