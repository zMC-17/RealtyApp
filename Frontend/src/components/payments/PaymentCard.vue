<!-- components/payments/PaymentCard.vue -->
<template>
    <div class="payment-card" :class="{
        'payment-card--attention': isAttention,
        'payment-card--overdue': payment.status === 'overdue'
    }">
        <div class="payment-card__header">
            <PaymentStatusBadge :status="payment.status" />
            <span class="payment-date">{{ formattedDate }}</span>
        </div>

        <div class="payment-card__body">
            <div class="payment-info">
                <div class="info-row">
                    <span class="info-icon">🏠</span>
                    <div class="info-content">
                        <span class="info-label">Объект</span>
                        <span class="info-value">{{ payment.property_info?.title || '—' }}</span>
                        <span class="info-sub">{{ payment.property_info?.address || '' }}</span>
                    </div>
                </div>

                <div class="info-row">
                    <span class="info-icon">👤</span>
                    <div class="info-content">
                        <span class="info-label">Арендатор</span>
                        <span class="info-value">{{ payment.tenant_info?.name || '—' }}</span>
                        <span class="info-sub">{{ payment.tenant_info?.email || '' }}</span>
                    </div>
                </div>

                <div class="info-row">
                    <span class="info-icon">💰</span>
                    <div class="info-content">
                        <span class="info-label">Сумма</span>
                        <span class="info-value info-value--amount">
                            {{ formattedAmount }}
                        </span>
                    </div>
                </div>

                <div v-if="payment.comment" class="info-row">
                    <span class="info-icon">💬</span>
                    <div class="info-content">
                        <span class="info-label">Комментарий</span>
                        <span class="info-value">{{ payment.comment }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Кнопки действий для платежей требующих подтверждения -->
        <div v-if="payment.status === 'waiting_confirmation'" class="payment-card__actions">
            <button class="btn-confirm" @click="$emit('confirm', payment.id)">
                ✅ Подтвердить
            </button>
            <button class="btn-reject" @click="$emit('reject', payment.id)">
                ❌ Отклонить
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PaymentResponse } from '../../types/payment';
import PaymentStatusBadge from './PaymentStatusBadge.vue';

const props = defineProps<{
    payment: PaymentResponse;
}>();

defineEmits<{
    confirm: [paymentId: number];
    reject: [paymentId: number];
}>();

const isAttention = computed(() =>
    props.payment.status === 'waiting_confirmation' || props.payment.status === 'overdue'
);

const formattedAmount = computed(() => {
    const amount = parseFloat(props.payment.amount);
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
    }).format(amount);
});

const formattedDate = computed(() => {
    return new Date(props.payment.due_date).toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });
});
</script>

<style scoped>
.payment-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.payment-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.payment-card--attention {
    border-left: 4px solid #3b82f6;
}

.payment-card--overdue {
    border-left: 4px solid #ef4444;
}

.payment-card__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #f3f4f6;
}

.payment-date {
    color: #6b7280;
    font-size: 0.875rem;
}

.payment-card__body {
    padding: 1.25rem;
}

.payment-info {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.info-row {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
}

.info-icon {
    font-size: 1.25rem;
    flex-shrink: 0;
    margin-top: 0.125rem;
}

.info-content {
    display: flex;
    flex-direction: column;
    gap: 0.125rem;
}

.info-label {
    font-size: 0.75rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.info-value {
    color: #1f2937;
    font-weight: 500;
}

.info-value--amount {
    font-size: 1.25rem;
    color: #059669;
    font-weight: 600;
}

.info-sub {
    color: #6b7280;
    font-size: 0.875rem;
}

.payment-card__actions {
    display: flex;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: #f9fafb;
    border-top: 1px solid #f3f4f6;
}

.btn-confirm,
.btn-reject {
    flex: 1;
    padding: 0.625rem;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

.btn-confirm {
    background: #10b981;
    color: white;
}

.btn-confirm:hover {
    background: #059669;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.btn-reject {
    background: #ef4444;
    color: white;
}

.btn-reject:hover {
    background: #dc2626;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}
</style>