<!-- components/properties/PropertyContract.vue -->
<template>
    <div class="property-contract">

        <!-- Договор есть -->
        <template v-if="contract">
            <div class="contract-panel">

                <!-- Шапка: номер + статус -->
                <div class="contract-header">
                    <div class="contract-id-wrap">
                        <span class="contract-eyebrow">Договор аренды</span>
                        <span class="contract-id">#{{ contract.id }}</span>
                    </div>
                    <span class="status-badge" :class="`status-badge--${contract.status}`">
                        {{ statusLabel }}
                    </span>
                </div>

                <!-- Данные -->
                <div class="contract-body">

                    <!-- Период -->
                    <div class="info-row">
                        <span class="info-label">Период аренды</span>
                        <span class="info-value">
                            {{ formatDate(contract.start_date) }} — {{ formatDate(contract.end_date) }}
                        </span>
                    </div>

                    <!-- Платёж -->
                    <div class="info-row">
                        <span class="info-label">Ежемесячный платёж</span>
                        <span class="info-value info-value--amount">
                            {{ formatCurrency(contract.monthly_payment) }}
                        </span>
                    </div>

                    <!-- Депозит -->
                    <div class="info-row" v-if="contract.security_deposit">
                        <span class="info-label">Депозит</span>
                        <span class="info-value">{{ formatCurrency(contract.security_deposit) }}</span>
                    </div>

                </div>
            </div>
        </template>

        <!-- Нет договора -->
        <template v-else>
            <div class="no-contract">
                <div class="no-contract-icon">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                        <rect x="4" y="2" width="20" height="24" rx="2" stroke="currentColor" stroke-width="1.5" />
                        <path d="M9 9h10M9 14h10M9 19h6" stroke="currentColor" stroke-width="1.5"
                            stroke-linecap="round" />
                    </svg>
                </div>
                <h3 class="no-contract-title">Договор отсутствует</h3>
                <p class="no-contract-text">Создайте договор, указав email арендатора и условия аренды</p>
                <button class="btn-create" @click="showCreateModal = true">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
                    </svg>
                    Создать договор
                </button>
            </div>

            <CreateContractModal v-if="showCreateModal" :property-id="propertyId" @close="showCreateModal = false"
                @created="onContractCreated" />
        </template>

    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { ContractResponse } from '../../types/contract';
import { CONTRACT_STATUS_LABELS } from '../../types/contract';
import CreateContractModal from './CreateContractModal.vue';

const props = defineProps<{ propertyId: number; contract: ContractResponse | null }>();
const emit = defineEmits<{ 'contract-created': [] }>();

const showCreateModal = ref(false);

const statusLabel = computed(() =>
    CONTRACT_STATUS_LABELS[props.contract?.status || ''] || props.contract?.status
);

const onContractCreated = () => {
    showCreateModal.value = false;
    emit('contract-created');
};

const formatDate = (d: string) =>
    new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });

const formatCurrency = (v: string) =>
    new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(parseFloat(v));
</script>

<style scoped>
/* ---- Панель договора ---- */
.contract-panel {
    background: rgba(255, 255, 255, 0.52);
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.70) inset, 0 8px 32px rgba(28, 26, 23, 0.08);
}

/* Изумрудная полоска сверху — активный договор */
.contract-panel::before {
    content: '';
    display: block;
    height: 3px;
    background: linear-gradient(90deg, var(--color-emerald), var(--color-olive));
}

/* ---- Шапка ---- */
.contract-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-5) var(--space-6);
    border-bottom: 1px solid rgba(28, 26, 23, 0.08);
}

.contract-id-wrap {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.contract-eyebrow {
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--color-dark-35);
}

.contract-id {
    font-size: var(--text-xl);
    font-weight: 800;
    color: var(--color-dark);
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
}

/* Статус-бейдж */
.status-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px var(--space-3);
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    white-space: nowrap;
}

.status-badge--active {
    background: var(--color-success-bg);
    color: var(--color-success);
}

.status-badge--pending {
    background: var(--color-warning-bg);
    color: var(--color-warning);
}

.status-badge--expired {
    background: var(--color-neutral-bg);
    color: var(--color-neutral);
}

.status-badge--cancelled {
    background: var(--color-danger-bg);
    color: var(--color-danger);
}

/* ---- Тело ---- */
.contract-body {
    padding: var(--space-5) var(--space-6);
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
}

/* Блоки участников */
.info-block {
    display: flex;
    align-items: flex-start;
    gap: var(--space-3);
    padding: var(--space-4);
    border-radius: var(--radius-md);
}

.info-block--accent {
    background: var(--color-emerald-08);
    border: 1px solid var(--color-emerald-20);
}

.info-block--muted {
    background: rgba(28, 26, 23, 0.04);
    border: 1px solid rgba(28, 26, 23, 0.08);
}

.info-block-icon {
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    border-radius: var(--radius-sm);
    background: rgba(255, 255, 255, 0.70);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-dark-60);
}

.info-block--accent .info-block-icon {
    color: var(--color-emerald);
}

.info-block>div {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.info-divider {
    height: 1px;
    background: rgba(28, 26, 23, 0.08);
    margin: var(--space-1) 0;
}

/* Строки данных */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: var(--space-6);
}

.info-label {
    font-size: var(--text-xs);
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-dark-35);
    flex-shrink: 0;
}

.info-value {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--color-dark);
    text-align: right;
}

.info-value--amount {
    font-size: var(--text-md);
    font-weight: 800;
    color: var(--color-emerald);
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
}

.info-sub {
    font-size: var(--text-xs);
    color: var(--color-dark-35);
}

/* ---- Нет договора ---- */
.no-contract {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-16) var(--space-8);
    text-align: center;
}

.no-contract-icon {
    width: 64px;
    height: 64px;
    border-radius: var(--radius-xl);
    background: rgba(255, 255, 255, 0.52);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.65);
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.70) inset, 0 6px 20px rgba(28, 26, 23, 0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-dark-35);
    margin-bottom: var(--space-2);
}

.no-contract-title {
    font-size: var(--text-lg);
    font-weight: 800;
    color: var(--color-dark);
    letter-spacing: -0.02em;
}

.no-contract-text {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
    max-width: 300px;
    line-height: 1.6;
}

.btn-create {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    margin-top: var(--space-2);
    padding: var(--space-3) var(--space-6);
    background: var(--color-emerald);
    color: #fff;
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 700;
    cursor: pointer;
    transition: all var(--transition);
}

.btn-create:hover {
    background: #155c3e;
    box-shadow: 0 4px 16px rgba(26, 107, 74, 0.30);
    transform: translateY(-1px);
}

.btn-create:active {
    transform: translateY(0);
}
</style>