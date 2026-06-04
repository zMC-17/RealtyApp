<!-- components/properties/EditPropertyModal.vue -->
<template>
    <div class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Редактировать объект</h2>
                <button class="modal-close" @click="$emit('close')">✕</button>
            </div>

            <form @submit.prevent="handleSubmit" class="modal-body">
                <div class="form-group">
                    <label for="editPropertyType">Тип недвижимости *</label>
                    <select id="editPropertyType" v-model="form.property_type" required :disabled="loading">
                        <option value="" disabled>Выберите тип</option>
                        <option v-for="type in PROPERTY_TYPES" :key="type.value" :value="type.value">
                            {{ type.label }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="editTitle">Название *</label>
                    <input id="editTitle" v-model="form.title" type="text" required minlength="3" maxlength="255"
                        :disabled="loading" />
                </div>

                <div class="form-group">
                    <label for="editAddress">Адрес *</label>
                    <input id="editAddress" v-model="form.address" type="text" required minlength="5" maxlength="255"
                        :disabled="loading" />
                </div>

                <div class="form-group">
                    <label for="editDescription">Описание</label>
                    <textarea id="editDescription" v-model="form.description" rows="4" maxlength="5000"
                        :disabled="loading" placeholder="Опишите особенности объекта..." />
                </div>

                <div v-if="error" class="error-message">
                    {{ error }}
                </div>

                <div class="modal-actions">
                    <button type="button" class="btn-cancel" @click="$emit('close')" :disabled="loading">
                        Отмена
                    </button>
                    <button type="submit" class="btn-submit" :disabled="loading">
                        {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import { propertiesService } from '../../services/properties';
import { usePropertiesStore } from '../../stores/properties';
import { PROPERTY_TYPES } from '../../types/property';
import type { PropertyResponse, PropertyCreate } from '../../types/property';

const props = defineProps<{
    property: PropertyResponse;
}>();

const emit = defineEmits<{
    close: [];
    updated: [property: PropertyResponse];
}>();

const propertiesStore = usePropertiesStore();
const loading = ref(false);
const error = ref('');

const form = reactive<PropertyCreate>({
    property_type: props.property.property_type,
    title: props.property.title,
    address: props.property.address,
    description: props.property.description || '',
});

const handleSubmit = async () => {
    loading.value = true;
    error.value = '';

    try {
        const updated = await propertiesService.updateProperty(props.property.id, form);
        emit('updated', updated);
    } catch (err: any) {
        error.value = err.response?.data?.detail || 'Ошибка обновления объекта';
    } finally {
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
}

.modal-content {
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
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
    color: #6b7280;
    cursor: pointer;
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
select,
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
    min-height: 100px;
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

.btn-submit:hover:not(:disabled) {
    background: #5a67d8;
}
</style>