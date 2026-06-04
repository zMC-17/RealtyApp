<!-- components/tenant/QuickInfo.vue -->
<template>
    <div class="quick-info">
        <div class="quick-card">
            <span class="quick-icon">📅</span>
            <div>
                <span class="quick-label">Следующий платёж</span>
                <strong>{{ nextPaymentDate }}</strong>
            </div>
        </div>

        <div class="quick-card">
            <span class="quick-icon">⏳</span>
            <div>
                <span class="quick-label">Осталось месяцев</span>
                <strong>{{ remainingMonths }}</strong>
            </div>
        </div>

        <div class="quick-card">
            <span class="quick-icon">💰</span>
            <div>
                <span class="quick-label">Ежемесячный платёж</span>
                <strong>{{ formatCurrency(contract.monthly_payment) }}</strong>
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
    return next.toLocaleDateString('ru-RU');
});

const remainingMonths = computed(() => {
    const now = new Date();
    const end = new Date(props.contract.end_date);
    return Math.max(0, (end.getFullYear() - now.getFullYear()) * 12 + (end.getMonth() - now.getMonth()));
});

const formatCurrency = (v: string) =>
    new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(parseFloat(v));
</script>

<style scoped>
.quick-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.quick-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
}

.quick-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.quick-label {
    display: block;
    font-size: 0.75rem;
    color: #9ca3af;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

strong {
    color: #1f2937;
}
</style>