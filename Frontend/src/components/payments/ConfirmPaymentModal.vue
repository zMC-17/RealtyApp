<!-- components/payments/ConfirmPaymentModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-box">

            <div class="modal-header">
                <span class="modal-title">Подтверждение платежа</span>
                <button class="modal-close" @click="$emit('close')">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5"
                            stroke-linecap="round" />
                    </svg>
                </button>
            </div>

            <div class="modal-body" v-if="payment">

                <!-- Предупреждение -->
                <div class="notice notice--warning">
                    Вы подтверждаете получение оплаты. Платёж будет отмечен как выполненный — действие необратимо.
                </div>

                <!-- Сводка -->
                <div class="summary-block">
                    <div class="summary-amount">{{ formattedAmount }}</div>
                    <div class="summary-rows">
                        <div class="summary-row">
                            <span class="summary-label">Объект</span>
                            <span class="summary-value">{{ payment.property_info?.title || '—' }}</span>
                        </div>
                        <div class="summary-row">
                            <span class="summary-label">Арендатор</span>
                            <span class="summary-value">{{ payment.tenant_info?.name || '—' }}</span>
                        </div>
                        <div class="summary-row">
                            <span class="summary-label">Дата платежа</span>
                            <span class="summary-value">{{ formattedDate }}</span>
                        </div>
                    </div>
                </div>

                <!-- Чек/комментарий арендатора -->
                <div v-if="payment.payment_proof_url" class="proof-block">
                    <span class="summary-label">Чек / комментарий арендатора</span>
                    <p class="proof-text">{{ payment.payment_proof_url }}</p>
                </div>

                <div v-if="paymentsStore.error" class="notice notice--danger">
                    {{ paymentsStore.error }}
                </div>

            </div>

            <div class="modal-footer">
                <button class="btn-cancel" @click="$emit('close')">Отмена</button>
                <button class="btn-confirm" @click="handleConfirm" :disabled="paymentsStore.loading">
                    <span v-if="paymentsStore.loading" class="btn-spinner"></span>
                    {{ paymentsStore.loading ? 'Подтверждение…' : 'Подтвердить оплату' }}
                </button>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePaymentsStore } from '../../stores/payments';
import type { PaymentResponse } from '../../types/payment';

const props = defineProps<{ visible: boolean; payment: PaymentResponse | null }>();
const emit = defineEmits<{ close: []; confirmed: [] }>();
const paymentsStore = usePaymentsStore();

const formattedAmount = computed(() => props.payment
    ? new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(parseFloat(props.payment.amount))
    : ''
);
const formattedDate = computed(() => props.payment
    ? new Date(props.payment.due_date).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
    : ''
);

const handleConfirm = async () => {
    if (!props.payment) return;
    const success = await paymentsStore.confirmPayment(props.payment.id);
    if (success) { emit('confirmed'); emit('close'); }
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(28, 26, 23, 0.40);
    backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeIn 180ms ease;
}

.modal-box {
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(32px) saturate(160%);
    -webkit-backdrop-filter: blur(32px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.80);
    border-radius: var(--radius-xl);
    width: 90%;
    max-width: 460px;
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.85) inset, 0 24px 60px rgba(28, 26, 23, 0.16);
    animation: slideUp 220ms ease;
    overflow: hidden;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-6) var(--space-6) var(--space-5);
    border-bottom: 1px solid rgba(28, 26, 23, 0.08);
}

.modal-title {
    font-size: var(--text-md);
    font-weight: 700;
    color: var(--color-dark);
    letter-spacing: -0.02em;
}

.modal-close {
    width: 28px;
    height: 28px;
    border-radius: var(--radius-sm);
    border: none;
    background: rgba(28, 26, 23, 0.06);
    color: var(--color-dark-60);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--transition);
}

.modal-close:hover {
    background: rgba(28, 26, 23, 0.12);
    color: var(--color-dark);
}

.modal-body {
    padding: var(--space-6);
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
}

/* ---- Notice ---- */
.notice {
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    font-size: var(--text-sm);
    font-weight: 500;
    line-height: 1.5;
}

.notice--warning {
    background: var(--color-warning-bg);
    color: var(--color-warning);
    border: 1px solid rgba(184, 115, 51, 0.18);
}

.notice--danger {
    background: var(--color-danger-bg);
    color: var(--color-danger);
    border: 1px solid rgba(185, 64, 64, 0.18);
}

/* ---- Сводка ---- */
.summary-block {
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.75);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
}

.summary-amount {
    font-size: var(--text-2xl);
    font-weight: 800;
    color: var(--color-emerald);
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
}

.summary-rows {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: var(--space-4);
}

.summary-label {
    font-size: var(--text-xs);
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-dark-35);
    flex-shrink: 0;
}

.summary-value {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--color-dark);
    text-align: right;
}

/* ---- Чек ---- */
.proof-block {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.proof-text {
    font-size: var(--text-sm);
    color: var(--color-dark-60);
    line-height: 1.55;
    word-break: break-word;
    padding: var(--space-3) var(--space-4);
    background: rgba(255, 255, 255, 0.45);
    border-radius: var(--radius-md);
    border: 1px solid rgba(255, 255, 255, 0.65);
}

/* ---- Футер ---- */
.modal-footer {
    display: flex;
    gap: var(--space-3);
    padding: var(--space-5) var(--space-6);
    border-top: 1px solid rgba(28, 26, 23, 0.08);
}

.btn-cancel {
    flex: 1;
    padding: var(--space-3);
    background: rgba(28, 26, 23, 0.06);
    border: 1px solid rgba(28, 26, 23, 0.10);
    border-radius: var(--radius-md);
    color: var(--color-dark-60);
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition);
}

.btn-cancel:hover {
    background: rgba(28, 26, 23, 0.10);
    color: var(--color-dark);
}

.btn-confirm {
    flex: 1;
    padding: var(--space-3);
    background: var(--color-emerald);
    border: none;
    border-radius: var(--radius-md);
    color: #fff;
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 700;
    cursor: pointer;
    transition: all var(--transition);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    letter-spacing: -0.01em;
}

.btn-confirm:hover:not(:disabled) {
    background: #155c3e;
    box-shadow: 0 4px 16px rgba(26, 107, 74, 0.30);
}

.btn-confirm:disabled {
    opacity: 0.45;
    cursor: not-allowed;
}

.btn-spinner {
    width: 13px;
    height: 13px;
    border: 2px solid rgba(255, 255, 255, 0.25);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
    flex-shrink: 0;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(16px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>