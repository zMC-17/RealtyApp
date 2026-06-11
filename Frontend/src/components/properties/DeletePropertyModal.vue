<!-- components/properties/DeletePropertyModal.vue -->
<template>
    <div class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-box">

            <div class="modal-header">
                <span class="modal-title">Удаление объекта</span>
                <button class="modal-close" @click="$emit('close')">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5"
                            stroke-linecap="round" />
                    </svg>
                </button>
            </div>

            <div class="modal-body">

                <!-- Иконка + название объекта -->
                <div class="danger-header">
                    <div class="danger-icon">
                        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                            <path d="M11 2L2 19h18L11 2Z" stroke="currentColor" stroke-width="1.5"
                                stroke-linejoin="round" />
                            <path d="M11 9v5M11 16v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                        </svg>
                    </div>
                    <div>
                        <p class="danger-object">{{ property.title }}</p>
                        <p class="danger-address">{{ property.address }}</p>
                    </div>
                </div>

                <!-- Последствия -->
                <div class="consequences">
                    <p class="consequences-title">Будет удалено безвозвратно</p>
                    <div class="consequences-list">
                        <div class="consequence-item">
                            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                                <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.4"
                                    stroke-linecap="round" />
                            </svg>
                            Все договоры аренды
                        </div>
                        <div class="consequence-item">
                            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                                <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.4"
                                    stroke-linecap="round" />
                            </svg>
                            Все платежи
                        </div>
                        <div class="consequence-item">
                            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                                <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.4"
                                    stroke-linecap="round" />
                            </svg>
                            Все заявки на обслуживание
                        </div>
                    </div>
                </div>

                <!-- Подтверждение вводом -->
                <div class="confirm-field">
                    <label class="field-label" for="confirmDelete">
                        Введите <strong class="confirm-word">УДАЛИТЬ</strong> для подтверждения
                    </label>
                    <input class="field-input" id="confirmDelete" v-model="confirmText" type="text"
                        placeholder="УДАЛИТЬ" :disabled="loading" @paste.prevent autocomplete="off" />
                </div>

                <div v-if="error" class="notice notice--danger">{{ error }}</div>

            </div>

            <div class="modal-footer">
                <button class="btn-cancel" @click="$emit('close')" :disabled="loading">
                    Отмена
                </button>
                <button class="btn-delete" :disabled="confirmText !== 'УДАЛИТЬ' || loading" @click="handleDelete">
                    <span v-if="loading" class="btn-spinner"></span>
                    {{ loading ? 'Удаление…' : 'Удалить объект' }}
                </button>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { propertiesService } from '../../services/properties';
import { usePropertiesStore } from '../../stores/properties';
import type { PropertyResponse } from '../../types/property';

const props = defineProps<{ property: PropertyResponse }>();
const emit = defineEmits<{ close: []; deleted: [] }>();

const propertiesStore = usePropertiesStore();
const loading = ref(false);
const error = ref('');
const confirmText = ref('');

const handleDelete = async () => {
    if (confirmText.value !== 'УДАЛИТЬ') return;
    loading.value = true; error.value = '';
    try {
        await propertiesService.deleteProperty(props.property.id);
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
    inset: 0;
    background: rgba(28, 26, 23, 0.45);
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
    max-width: 440px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.85) inset, 0 24px 60px rgba(28, 26, 23, 0.18);
    animation: slideUp 220ms ease;
    overflow: hidden;
    /* Тонкая красная полоска сверху — сигнал опасности */
    border-top: 2px solid var(--color-danger);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-5) var(--space-6);
    border-bottom: 1px solid rgba(28, 26, 23, 0.08);
}

.modal-title {
    font-size: var(--text-md);
    font-weight: 700;
    color: var(--color-danger);
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

/* ---- Иконка + объект ---- */
.danger-header {
    display: flex;
    align-items: flex-start;
    gap: var(--space-4);
}

.danger-icon {
    flex-shrink: 0;
    width: 44px;
    height: 44px;
    border-radius: var(--radius-md);
    background: var(--color-danger-bg);
    border: 1px solid rgba(185, 64, 64, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-danger);
}

.danger-object {
    font-size: var(--text-base);
    font-weight: 700;
    color: var(--color-dark);
    margin-bottom: 2px;
}

.danger-address {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
}

/* ---- Последствия ---- */
.consequences {
    background: var(--color-danger-bg);
    border: 1px solid rgba(185, 64, 64, 0.15);
    border-radius: var(--radius-md);
    padding: var(--space-4) var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.consequences-title {
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-danger);
}

.consequences-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.consequence-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-sm);
    color: var(--color-danger);
    font-weight: 500;
}

.consequence-item svg {
    flex-shrink: 0;
    opacity: 0.7;
}

/* ---- Поле подтверждения ---- */
.confirm-field {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.field-label {
    font-size: var(--text-xs);
    color: var(--color-dark-60);
    font-weight: 500;
    line-height: 1.5;
}

.confirm-word {
    color: var(--color-danger);
    font-weight: 800;
    letter-spacing: 0.05em;
}

.field-input {
    width: 100%;
    padding: var(--space-3) var(--space-4);
    background: rgba(255, 255, 255, 0.65);
    border: 1.5px solid rgba(28, 26, 23, 0.12);
    border-radius: var(--radius-md);
    color: var(--color-dark);
    font-family: var(--font-base);
    font-size: var(--text-base);
    font-weight: 700;
    letter-spacing: 0.08em;
    text-align: center;
    transition: border-color var(--transition), box-shadow var(--transition);
}

.field-input:focus {
    outline: none;
    border-color: rgba(185, 64, 64, 0.40);
    box-shadow: 0 0 0 3px var(--color-danger-bg);
}

.field-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
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

.btn-delete {
    flex: 1;
    padding: var(--space-3);
    background: var(--color-danger);
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
}

.btn-delete:hover:not(:disabled) {
    background: #9b2a2a;
    box-shadow: 0 4px 16px rgba(185, 64, 64, 0.30);
}

.btn-delete:disabled {
    opacity: 0.40;
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