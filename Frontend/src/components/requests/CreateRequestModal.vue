<!-- components/requests/CreateRequestModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Создать заявку</h2>
                <button class="modal-close" @click="$emit('close')">✕</button>
            </div>

            <form @submit.prevent="handleSubmit" class="modal-body">
                <div class="form-group">
                    <label for="requestTitle">Заголовок *</label>
                    <input id="requestTitle" v-model="title" type="text" required minlength="3" maxlength="255"
                        placeholder="Например: Протекает кран в ванной" />
                </div>

                <div class="form-group">
                    <label for="requestMessage">Описание *</label>
                    <textarea id="requestMessage" v-model="message" rows="5" required minlength="5" maxlength="5000"
                        placeholder="Опишите проблему подробнее..." />
                    <span class="char-count">{{ message.length }}/5000</span>
                </div>

                <div v-if="error" class="error-message">{{ error }}</div>

                <div class="modal-actions">
                    <button type="button" class="btn-cancel" @click="$emit('close')">Отмена</button>
                    <button type="submit" class="btn-submit" :disabled="!canSubmit || sending">
                        {{ sending ? 'Создание...' : 'Создать заявку' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { requestsService } from '../../services/requests';

const props = defineProps<{
    visible: boolean;
    contractId: number;
}>();

const emit = defineEmits<{
    close: [];
    created: [];
}>();

const title = ref('');
const message = ref('');
const sending = ref(false);
const error = ref('');

const canSubmit = computed(() => title.value.trim().length >= 3 && message.value.trim().length >= 5);

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
    max-width: 500px;
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

.form-group {
    margin-bottom: 1.25rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

input,
textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 0.95rem;
    box-sizing: border-box;
}

textarea {
    resize: vertical;
    min-height: 120px;
}

input:focus,
textarea:focus {
    outline: none;
    border-color: #667eea;
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
    color: #dc2626;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 1rem;
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
    font-weight: 500;
    cursor: pointer;
}

.btn-cancel {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
}

.btn-submit {
    background: #667eea;
    border: none;
    color: white;
}

.btn-submit:disabled {
    opacity: 0.5;
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