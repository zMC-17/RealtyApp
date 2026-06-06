<!-- components/payments/RequestConfirmationModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Подтверждение оплаты</h2>
                <button class="modal-close" @click="$emit('close')">✕</button>
            </div>

            <div class="modal-body">
                <div class="payment-info">
                    <div class="info-row">
                        <span>Сумма:</span>
                        <strong>{{ formatCurrency(payment.amount) }}</strong>
                    </div>
                    <div class="info-row">
                        <span>Дата платежа:</span>
                        <strong>{{ formatDate(payment.due_date) }}</strong>
                    </div>
                </div>

                <div class="form-group">
                    <label for="proofText">
                        Ссылка на чек или комментарий *
                    </label>
                    <textarea id="proofText" v-model="proofText" rows="4" required minlength="3" maxlength="2000"
                        placeholder="Например: ссылка на чек в облаке или комментарий об оплате" />
                    <span class="char-count">{{ proofText.length }}/2000</span>
                </div>

                <div v-if="error" class="error-message">{{ error }}</div>
            </div>

            <div class="modal-actions">
                <button class="btn-cancel" @click="$emit('close')" :disabled="sending">
                    Отмена
                </button>
                <button class="btn-submit" :disabled="!canSubmit || sending" @click="handleSubmit">
                    {{ sending ? 'Отправка...' : 'Отправить на проверку' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { paymentsService } from '../../services/payments';
import type { PaymentResponse } from '../../types/payment';

const props = defineProps<{
    visible: boolean;
    payment: PaymentResponse;
}>();

const emit = defineEmits<{
    close: [];
    sent: [];
}>();

const proofText = ref('');
const sending = ref(false);
const error = ref('');

const canSubmit = computed(() => proofText.value.trim().length >= 3);

const handleSubmit = async () => {
    if (!canSubmit.value) return;

    sending.value = true;
    error.value = '';

    try {
        await paymentsService.requestConfirmation(props.payment.id, {
            payment_proof_url: proofText.value.trim(),
            comment: proofText.value.trim(),
        });

        emit('sent');
    } catch (err: any) {
        error.value = err.response?.data?.detail || 'Ошибка отправки';
    } finally {
        sending.value = false;
    }
};

const formatCurrency = (v: string) =>
    new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
    }).format(parseFloat(v));

const formatDate = (d: string) => new Date(d).toLocaleDateString('ru-RU');
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
    animation: fadeIn 0.2s ease;
}

.modal-content {
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 480px;
    max-height: 90vh;
    overflow-y: auto;
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
    color: #1f2937;
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #6b7280;
    cursor: pointer;
    padding: 0.25rem;
    transition: color 0.2s;
}

.modal-close:hover {
    color: #1f2937;
}

.modal-body {
    padding: 1.5rem;
}

.payment-info {
    background: #f9fafb;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.375rem 0;
    color: #374151;
}

.info-row strong {
    color: #1f2937;
}

.form-group {
    margin-bottom: 1.25rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
    font-size: 0.9rem;
}

textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 0.95rem;
    resize: vertical;
    min-height: 100px;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-sizing: border-box;
}

textarea:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.char-count {
    display: block;
    text-align: right;
    color: #9ca3af;
    font-size: 0.8rem;
    margin-top: 0.25rem;
}

.error-message {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.875rem;
}

.modal-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
    margin-top: 1.5rem;
}

.btn-cancel,
.btn-submit {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-cancel {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    color: #374151;
}

.btn-cancel:hover:not(:disabled) {
    background: #e5e7eb;
}

.btn-submit {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
}

.btn-submit:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled,
.btn-cancel:disabled {
    opacity: 0.5;
    cursor: not-allowed;
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
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>