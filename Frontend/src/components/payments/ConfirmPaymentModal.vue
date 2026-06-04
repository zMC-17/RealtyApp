<!-- components/payments/ConfirmPaymentModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Подтверждение платежа</h2>
                <button class="modal-close" @click="$emit('close')">✕</button>
            </div>

            <div class="modal-body">
                <div class="warning-message">
                    ⚠️ Вы подтверждаете получение оплаты. Это действие отметит платёж как выполненный.
                </div>

                <div v-if="payment" class="payment-summary">
                    <div class="summary-row">
                        <span>Сумма:</span>
                        <strong>{{ formattedAmount }}</strong>
                    </div>
                    <div class="summary-row">
                        <span>Объект:</span>
                        <strong>{{ payment.property_info?.title }}</strong>
                    </div>
                    <div class="summary-row">
                        <span>Арендатор:</span>
                        <strong>{{ payment.tenant_info?.name }}</strong>
                    </div>
                    <div class="summary-row">
                        <span>Дата платежа:</span>
                        <strong>{{ formattedDate }}</strong>
                    </div>
                </div>

                <div v-if="payment?.payment_proof_url" class="proof-section">
                    <div v-if="payment.payment_proof_url" class="proof-text">
                        <span class="proof-label">Чек/Комментарий:</span>
                        <p class="proof-content">{{ payment.payment_proof_url }}</p>
                    </div>
                </div>

                <div v-if="paymentsStore.error" class="error-message">
                    {{ paymentsStore.error }}
                </div>
            </div>

            <div class="modal-actions">
                <button class="btn-cancel" @click="$emit('close')">Отмена</button>
                <button class="btn-confirm" @click="handleConfirm" :disabled="paymentsStore.loading">
                    {{ paymentsStore.loading ? 'Подтверждение...' : 'Подтвердить оплату' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePaymentsStore } from '../../stores/payments';
import type { PaymentResponse } from '../../types/payment';

const props = defineProps<{
    visible: boolean;
    payment: PaymentResponse | null;
}>();

const emit = defineEmits<{
    close: [];
    confirmed: [];
}>();

const paymentsStore = usePaymentsStore();

const formattedAmount = computed(() => {
    if (!props.payment) return '';
    const amount = parseFloat(props.payment.amount);
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
    }).format(amount);
});

const formattedDate = computed(() => {
    if (!props.payment) return '';
    return new Date(props.payment.due_date).toLocaleDateString('ru-RU');
});

const handleConfirm = async () => {
    if (!props.payment) return;

    const success = await paymentsStore.confirmPayment(props.payment.id);
    if (success) {
        emit('confirmed');
        emit('close');
    }
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 480px;
    animation: slideUp 0.3s ease;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
    margin: 0;
    font-size: 1.25rem;
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #6b7280;
}

.modal-body {
    padding: 1.5rem;
}

.warning-message {
    padding: 0.75rem;
    background: #fef3c7;
    border: 1px solid #fbbf24;
    border-radius: 8px;
    color: #92400e;
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
}

.payment-summary {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #374151;
}

.proof-section {
    padding: 1rem;
    background: #f3f4f6;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.proof-section h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
}

.proof-link {
    color: #3b82f6;
    text-decoration: none;
}

.proof-link:hover {
    text-decoration: underline;
}

.error-message {
    padding: 0.75rem;
    background: #fee2e2;
    color: #991b1b;
    border-radius: 8px;
    font-size: 0.875rem;
}

.modal-actions {
    display: flex;
    gap: 0.75rem;
    padding: 1.5rem;
    border-top: 1px solid #e5e7eb;
}

.btn-cancel,
.btn-confirm {
    flex: 1;
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-cancel {
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    color: #374151;
}

.btn-confirm {
    background: #10b981;
    border: none;
    color: white;
}

.btn-confirm:hover:not(:disabled) {
    background: #059669;
}

.btn-confirm:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>