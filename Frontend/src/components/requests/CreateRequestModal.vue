<!-- components/requests/CreateRequestModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-box">

            <div class="modal-header">
                <span class="modal-title">Новая заявка</span>
                <button class="modal-close" @click="$emit('close')">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5"
                            stroke-linecap="round" />
                    </svg>
                </button>
            </div>

            <form @submit.prevent="handleSubmit" class="modal-body">

                <div class="field">
                    <label class="field-label" for="requestTitle">Заголовок *</label>
                    <input class="field-input" id="requestTitle" v-model="title" type="text" required minlength="3"
                        maxlength="255" placeholder="Например: протекает кран в ванной" />
                </div>

                <div class="field">
                    <label class="field-label" for="requestMessage">Описание *</label>
                    <textarea class="field-input field-textarea" id="requestMessage" v-model="message" rows="5" required
                        minlength="5" maxlength="5000"
                        placeholder="Опишите проблему подробнее — когда появилась, насколько срочно…" />
                    <span class="field-hint">{{ message.length }} / 5000</span>
                </div>

                <div v-if="error" class="notice notice--danger">{{ error }}</div>

            </form>

            <div class="modal-footer">
                <button class="btn-cancel" type="button" @click="$emit('close')">
                    Отмена
                </button>
                <button class="btn-confirm" type="button" :disabled="!canSubmit || sending" @click="handleSubmit">
                    <span v-if="sending" class="btn-spinner"></span>
                    {{ sending ? 'Создание…' : 'Создать заявку' }}
                </button>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { requestsService } from '../../services/requests';

const props = defineProps<{ visible: boolean; contractId: number }>();
const emit = defineEmits<{ close: []; created: [] }>();

const title = ref('');
const message = ref('');
const sending = ref(false);
const error = ref('');

const canSubmit = computed(() =>
    title.value.trim().length >= 3 && message.value.trim().length >= 5
);

const handleSubmit = async () => {
    if (!canSubmit.value) return;
    sending.value = true;
    error.value = '';
    try {
        await requestsService.createRequest({
            contract_id: props.contractId,
            title: title.value.trim(),
            message: message.value.trim(),
        });
        emit('created');
    } catch (err: any) {
        error.value = err.response?.data?.detail || 'Ошибка создания заявки';
    } finally {
        sending.value = false;
    }
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
    max-width: 480px;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.85) inset, 0 24px 60px rgba(28, 26, 23, 0.16);
    animation: slideUp 220ms ease;
    overflow: hidden;
}

/* ---- Шапка ---- */
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

/* ---- Тело ---- */
.modal-body {
    padding: var(--space-6);
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
    overflow-y: auto;
    flex: 1;
}

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
    min-height: 120px;
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

.btn-cancel:hover {
    background: rgba(28, 26, 23, 0.10);
    color: var(--color-dark);
}

.btn-confirm {
    flex: 1;
    padding: var(--space-3);
    background: var(--color-dark);
    border: none;
    border-radius: var(--radius-md);
    color: var(--color-bg);
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
    background: #2d2b27;
    box-shadow: 0 4px 16px rgba(28, 26, 23, 0.22);
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