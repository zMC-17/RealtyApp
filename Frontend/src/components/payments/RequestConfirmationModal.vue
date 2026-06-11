<!-- components/payments/RequestConfirmationModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-box">

            <div class="modal-header">
                <span class="modal-title">Подтверждение оплаты</span>
                <button class="modal-close" @click="$emit('close')">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5"
                            stroke-linecap="round" />
                    </svg>
                </button>
            </div>

            <div class="modal-body">

                <!-- Сводка платежа -->
                <div class="summary-block">
                    <div class="summary-amount">{{ formatCurrency(payment.amount) }}</div>
                    <div class="summary-row">
                        <span class="summary-label">Дата платежа</span>
                        <span class="summary-value">{{ formatDate(payment.due_date) }}</span>
                    </div>
                </div>

                <!-- Поле чека -->
                <div class="field">
                    <label class="field-label" for="proofText">
                        Ссылка на чек или комментарий *
                    </label>
                    <textarea class="field-input field-textarea" id="proofText" v-model="proofText" rows="4" required
                        minlength="3" maxlength="2000"
                        placeholder="Например: ссылка на чек в облаке или комментарий об оплате" />
                    <span class="field-hint">{{ proofText.length }} / 2000</span>
                </div>

                <div v-if="error" class="notice notice--danger">{{ error }}</div>

            </div>

            <div class="modal-footer">
                <button class="btn-cancel" @click="$emit('close')" :disabled="sending">
                    Отмена
                </button>
                <button class="btn-confirm" :disabled="!canSubmit || sending" @click="handleSubmit">
                    <span v-if="sending" class="btn-spinner"></span>
                    {{ sending ? 'Отправка…' : 'Отправить на проверку' }}
                </button>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { paymentsService } from '../../services/payments';
import type { PaymentResponse } from '../../types/payment';

const props = defineProps<{ visible: boolean; payment: PaymentResponse }>();
const emit = defineEmits<{ close: []; sent: [] }>();

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
        style: 'currency', currency: 'RUB', minimumFractionDigits: 0,
    }).format(parseFloat(v));

const formatDate = (d: string) =>
    new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
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
    max-height: 90vh;
    display: flex;
    flex-direction: column;
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
    flex-shrink: 0;
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
    overflow-y: auto;
    flex: 1;
}

/* ---- Сводка ---- */
.summary-block {
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.75);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.summary-amount {
    font-size: var(--text-2xl);
    font-weight: 800;
    color: var(--color-emerald);
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
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
}

.summary-value {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--color-dark);
}

/* ---- Поле ---- */
.field {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.field-label {
    font-size: var(--text-xs);
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-dark-35);
}

.field-input {
    width: 100%;
    padding: var(--space-3) var(--space-4);
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(28, 26, 23, 0.12);
    border-radius: var(--radius-md);
    color: var(--color-dark);
    font-family: var(--font-base);
    font-size: var(--text-base);
    transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
}

.field-input::placeholder {
    color: var(--color-dark-35);
}

.field-input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.90);
    border-color: var(--color-emerald-20);
    box-shadow: 0 0 0 3px var(--color-emerald-08);
}

.field-textarea {
    resize: vertical;
    min-height: 100px;
}

.field-hint {
    font-size: var(--text-xs);
    color: var(--color-dark-35);
    text-align: right;
}

.notice--danger {
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    background: var(--color-danger-bg);
    color: var(--color-danger);
    border: 1px solid rgba(185, 64, 64, 0.18);
    font-size: var(--text-sm);
    font-weight: 500;
}

/* ---- Футер ---- */
.modal-footer {
    display: flex;
    gap: var(--space-3);
    padding: var(--space-5) var(--space-6);
    border-top: 1px solid rgba(28, 26, 23, 0.08);
    flex-shrink: 0;
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

.btn-cancel:hover:not(:disabled) {
    background: rgba(28, 26, 23, 0.10);
    color: var(--color-dark);
}

.btn-cancel:disabled {
    opacity: 0.4;
    cursor: not-allowed;
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