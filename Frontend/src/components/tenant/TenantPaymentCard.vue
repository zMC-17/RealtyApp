<!-- components/tenant/TenantPaymentCard.vue -->
<template>
    <div class="payment-card" :class="`payment-card--${payment.status}`">
        <div class="payment-card__left">
            <div class="payment-date">
                <span class="date-day">{{ day }}</span>
                <span class="date-month">{{ month }}</span>
            </div>
        </div>

        <div class="payment-card__center">
            <div class="payment-amount">{{ formatCurrency(payment.amount) }}</div>
            <div class="payment-status">
                <PaymentStatusBadge :status="payment.status" />
            </div>
        </div>

        <div class="payment-card__right">
            <!-- Кнопка отправки чека (только для pending и overdue) -->
            <button v-if="canSendProof" class="btn-send-proof" @click="$emit('sendProof', payment.id)">
                📎 Чек
            </button>

            <!-- Ожидает подтверждения -->
            <span v-else-if="payment.status === 'waiting_confirmation'" class="waiting-text">
                ⏳ Ожидает
            </span>

            <!-- Оплачено -->
            <span v-else-if="payment.status === 'paid'" class="paid-icon">✅</span>
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
    props.payment.status === 'pending' || props.payment.status === 'overdue'
);

const day = computed(() => {
    const d = new Date(props.payment.due_date);
    return d.getDate();
});

const month = computed(() => {
    const d = new Date(props.payment.due_date);
    return d.toLocaleDateString('ru-RU', { month: 'short' }).replace('.', '');
});

const formatCurrency = (v: string) =>
    new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0,
    }).format(parseFloat(v));
</script>

<style scoped>
.payment-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s;
}

.payment-card:hover {
    transform: translateY(-1px);
}

.payment-card--overdue {
    border-left: 4px solid #ef4444;
    background: #fef2f2;
}

.payment-card--pending {
    border-left: 4px solid #f59e0b;
}

.payment-card--waiting_confirmation {
    border-left: 4px solid #3b82f6;
    background: #eff6ff;
}

.payment-card--paid {
    opacity: 0.7;
    background: #f9fafb;
}

.payment-card__left {
    flex-shrink: 0;
    text-align: center;
    min-width: 50px;
}

.date-day {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f2937;
    line-height: 1;
}

.date-month {
    display: block;
    font-size: 0.8rem;
    color: #6b7280;
    text-transform: capitalize;
}

.payment-card__center {
    flex: 1;
}

.payment-amount {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 0.25rem;
}

.payment-card__right {
    flex-shrink: 0;
}

.btn-send-proof {
    padding: 0.5rem 1rem;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-send-proof:hover {
    background: #5a67d8;
}

.waiting-text {
    font-size: 0.8rem;
    color: #2563eb;
}

.paid-icon {
    font-size: 1.5rem;
}
</style>