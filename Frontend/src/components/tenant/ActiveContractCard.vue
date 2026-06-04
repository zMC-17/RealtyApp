<!-- components/tenant/ActiveContractCard.vue -->
<template>
    <div class="active-card">
        <div class="active-card__header">
            <div class="status-badge status--active">Активен</div>
        </div>

        <div class="active-card__body">
            <div class="info-row">
                <span class="info-icon">🏠</span>
                <div>
                    <span class="info-label">Объект</span>
                    <strong>{{ contract.property_info?.title }}</strong>
                    <p class="info-sub">{{ contract.property_info?.address }}</p>
                </div>
            </div>

            <div class="info-row">
                <span class="info-icon">👤</span>
                <div>
                    <span class="info-label">Владелец</span>
                    <strong>{{ contract.owner_info?.name }}</strong>
                    <p class="info-sub">{{ contract.owner_info?.email }}</p>
                </div>
            </div>

            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Период</span>
                    <strong>{{ formatDate(contract.start_date) }} — {{ formatDate(contract.end_date) }}</strong>
                </div>
                <div class="info-item">
                    <span class="info-label">Платёж</span>
                    <strong class="amount">{{ formatCurrency(contract.monthly_payment) }}/мес</strong>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { ContractWithDetails } from '../../types/contract';

defineProps<{ contract: ContractWithDetails }>();

const formatDate = (d: string) => new Date(d).toLocaleDateString('ru-RU');
const formatCurrency = (v: string) =>
    new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(parseFloat(v));
</script>

<style scoped>
.active-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin-bottom: 1.5rem;
}

.active-card__header {
    padding: 1rem 1.5rem;
    background: linear-gradient(135deg, #10b981, #059669);
}

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
}

.active-card__body {
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
}

.amount {
    color: #059669;
}
</style>