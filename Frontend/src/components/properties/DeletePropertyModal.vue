<!-- components/properties/DeletePropertyModal.vue -->
<template>
    <div class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Удаление объекта</h2>
                <button class="modal-close" @click="$emit('close')">✕</button>
            </div>

            <div class="modal-body">
                <div class="warning-icon">⚠️</div>

                <h3 class="warning-title">Вы уверены?</h3>

                <p class="warning-text">
                    Вы собираетесь удалить объект недвижимости
                    <strong>«{{ property.title }}»</strong>
                    по адресу <strong>{{ property.address }}</strong>.
                </p>

                <div class="warning-box">
                    <p><strong>Это действие:</strong></p>
                    <ul>
                        <li>Удалит все связанные договоры</li>
                        <li>Удалит все связанные платежи</li>
                        <li>Удалит все связанные заявки</li>
                        <li>Не может быть отменено</li>
                    </ul>
                </div>

                <div class="confirm-section">
                    <label for="confirmDelete">
                        Введите <strong>УДАЛИТЬ</strong> для подтверждения:
                    </label>
                    <input id="confirmDelete" v-model="confirmText" type="text" placeholder="УДАЛИТЬ"
                        :disabled="loading" @paste.prevent />
                </div>

                <div v-if="error" class="error-message">
                    {{ error }}
                </div>

                <div class="modal-actions">
                    <button type="button" class="btn-cancel" @click="$emit('close')" :disabled="loading">
                        Отмена
                    </button>
                    <button class="btn-delete" :disabled="confirmText !== 'УДАЛИТЬ' || loading" @click="handleDelete">
                        {{ loading ? 'Удаление...' : 'Удалить объект' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { propertiesService } from '../../services/properties';
import { usePropertiesStore } from '../../stores/properties';
import type { PropertyResponse } from '../../types/property';

const props = defineProps<{
    property: PropertyResponse;
}>();

const emit = defineEmits<{
    close: [];
    deleted: [];
}>();

const propertiesStore = usePropertiesStore();
const loading = ref(false);
const error = ref('');
const confirmText = ref('');

const handleDelete = async () => {
    if (confirmText.value !== 'УДАЛИТЬ') return;

    loading.value = true;
    error.value = '';

    try {
        await propertiesService.deleteProperty(props.property.id);
        // Обновляем список объектов в сторе
        await propertiesStore.fetchProperties();
        emit('deleted');
    } catch (err: any) {
        error.value = err.response?.data?.detail || 'Ошибка удаления объекта';
        loading.value = false;
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
    color: #dc2626;
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

.warning-icon {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 1rem;
}

.warning-title {
    text-align: center;
    color: #1f2937;
    margin: 0 0 1rem 0;
    font-size: 1.25rem;
}

.warning-text {
    text-align: center;
    color: #6b7280;
    margin: 0 0 1.5rem 0;
    line-height: 1.5;
}

.warning-box {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
}

.warning-box p {
    margin: 0 0 0.5rem 0;
    color: #991b1b;
}

.warning-box ul {
    margin: 0;
    padding-left: 1.25rem;
    color: #7f1d1d;
}

.warning-box li {
    margin-bottom: 0.25rem;
    font-size: 0.875rem;
}

.confirm-section {
    margin-bottom: 1.5rem;
}

.confirm-section label {
    display: block;
    margin-bottom: 0.5rem;
    color: #374151;
    font-size: 0.9rem;
}

.confirm-section input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #d1d5db;
    border-radius: 8px;
    font-size: 1rem;
    text-align: center;
    font-weight: 600;
    letter-spacing: 0.1em;
    box-sizing: border-box;
    transition: border-color 0.2s;
}

.confirm-section input:focus {
    outline: none;
    border-color: #dc2626;
}

.confirm-section input:disabled {
    background: #f9fafb;
    cursor: not-allowed;
}

.error-message {
    background: #fef2f2;
    color: #dc2626;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.875rem;
}

.modal-actions {
    display: flex;
    gap: 0.75rem;
}

.btn-cancel,
.btn-delete {
    flex: 1;
    padding: 0.75rem;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    font-size: 0.95rem;
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

.btn-delete {
    background: #dc2626;
    border: none;
    color: white;
}

.btn-delete:hover:not(:disabled) {
    background: #b91c1c;
}

.btn-delete:disabled {
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