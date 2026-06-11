<!-- components/tenant/TenantPaymentCard.vue -->
<template>
    <div class="payment-row" :class="{
        'payment-row--overdue': payment.status === 'overdue',
        'payment-row--pending': payment.status === 'pending',
        'payment-row--waiting': payment.status === 'waiting_confirmation',
        'payment-row--paid': payment.status === 'paid',
    }">
        <div class="row-accent"></div>

        <!-- Дата -->
        <div class="row-date">
            <span class="date-day">{{ day }}</span>
            <span class="date-month">{{ month }}</span>
        </div>

        <!-- Статус -->
        <div class="row-status">
            <PaymentStatusBadge :status="payment.status" />
        </div>

        <!-- Сумма -->
        <div class="row-amount">{{ formatCurrency(payment.amount) }}</div>

        <!-- Действие -->
        <div class="row-action">

            <!-- Отправить чек -->
            <button v-if="canSendProof" class="btn-proof" @click.stop="$emit('sendProof', payment.id)">
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <path d="M2 6.5L4.5 9 11 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                        stroke-linejoin="round" />
                    <path d="M1 9.5L3.5 12 10 6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"
                        stroke-linejoin="round" opacity="0.7" />
                </svg>
                Подтвердить
            </button>

            <!-- Ожидает -->
            <span v-else-if="payment.status === 'waiting_confirmation'" class="status-hint status-hint--waiting">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <circle cx="6" cy="6" r="4.5" stroke="currentColor" stroke-width="1.2" />
                    <path d="M6 3.5v3l1.5 1.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"
                        stroke-linejoin="round" />
                </svg>
                Ожидает проверки
            </span>

            <!-- Оплачено -->
            <span v-else-if="payment.status === 'paid'" class="status-hint status-hint--paid">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path d="M2 6.5l3 3 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                        stroke-linejoin="round" />
                </svg>
                Оплачено
            </span>

        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PaymentResponse } from '../../types/payment';
import PaymentStatusBadge from '../payments/PaymentStatusBadge.vue';

const props = defineProps<{ payment: PaymentResponse }>();
defineEmits<{ sendProof: [paymentId: number] }>();

const canSendProof = computed(() =>
    ['pending', 'overdue'].includes(props.payment.status)
);

const day = computed(() => new Date(props.payment.due_date).getDate());
const month = computed(() =>
    new Date(props.payment.due_date).toLocaleDateString('ru-RU', { month: 'short' }).replace('.', '')
);

const formatCurrency = (v: string) =>
    new Intl.NumberFormat('ru-RU', {
        style: 'currency', currency: 'RUB', minimumFractionDigits: 0,
    }).format(parseFloat(v));
</script>

<style scoped>
/*
  Горизонтальная строка — та же схема что у PaymentCard владельца,
  но колонки другие: [полоска] [дата] [статус] [сумма] [действие]
*/
.payment-row {
    display: grid;
    grid-template-columns: 3px 52px 1fr auto auto;
    align-items: center;
    gap: var(--space-4);

    background: rgba(255, 255, 255, 0.50);
    backdrop-filter: blur(16px) saturate(130%);
    -webkit-backdrop-filter: blur(16px) saturate(130%);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: var(--radius-md);
    padding: var(--space-4) var(--space-5) var(--space-4) 0;
    overflow: hidden;

    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.65) inset, 0 2px 8px rgba(28, 26, 23, 0.05);
    transition: box-shadow var(--transition), border-color var(--transition);
}

.payment-row:hover {
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.80) inset, 0 6px 20px rgba(28, 26, 23, 0.09);
    border-color: rgba(255, 255, 255, 0.82);
}

/* Оплаченные — чуть приглушены */
.payment-row--paid {
    opacity: 0.65;
}

/* ---- Полоска ---- */
.row-accent {
    height: 100%;
    min-height: 52px;
    border-radius: 0 2px 2px 0;
    background: transparent;
}

.payment-row--overdue .row-accent {
    background: var(--color-danger);
}

.payment-row--pending .row-accent {
    background: var(--color-warning);
}

.payment-row--waiting .row-accent {
    background: var(--color-info);
}

.payment-row--paid .row-accent {
    background: var(--color-emerald);
}

/* ---- Дата ---- */
.row-date {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1px;
    flex-shrink: 0;
}

.date-day {
    font-size: var(--text-xl);
    font-weight: 800;
    color: var(--color-dark);
    line-height: 1;
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
}

.date-month {
    font-size: var(--text-xs);
    font-weight: 500;
    color: var(--color-dark-35);
    text-transform: capitalize;
}

/* ---- Статус ---- */
.row-status {
    min-width: 0;
}

/* ---- Сумма ---- */
.row-amount {
    font-size: var(--text-lg);
    font-weight: 800;
    color: var(--color-dark);
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}

/* Просроченные — красным */
.payment-row--overdue .row-amount {
    color: var(--color-danger);
}

/* ---- Действие ---- */
.row-action {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    min-width: 140px;
}

.btn-proof {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    background: var(--color-dark);
    color: var(--color-bg);
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-base);
    font-size: var(--text-xs);
    font-weight: 700;
    cursor: pointer;
    transition: all var(--transition);
    letter-spacing: -0.01em;
    white-space: nowrap;
}

.btn-proof:hover {
    background: #2d2b27;
    box-shadow: 0 3px 12px rgba(28, 26, 23, 0.22);
    transform: translateY(-1px);
}

.btn-proof:active {
    transform: translateY(0);
}

.status-hint {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-xs);
    font-weight: 600;
    white-space: nowrap;
}

.status-hint--waiting {
    color: var(--color-info);
}

.status-hint--paid {
    color: var(--color-emerald);
}
</style>