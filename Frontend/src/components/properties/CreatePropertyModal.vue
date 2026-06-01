<!-- components/properties/CreatePropertyModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Добавить новый объект</h2>
                <button class="modal-close" @click="$emit('close')">✕</button>
            </div>

            <form @submit.prevent="handleSubmit" class="modal-body">
                <div class="form-group">
                    <label for="propertyType">Тип недвижимости *</label>
                    <select id="propertyType" v-model="form.property_type" required>
                        <option value="" disabled>Выберите тип</option>
                        <option v-for="type in PROPERTY_TYPES" :key="type.value" :value="type.value">
                            {{ type.label }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="title">Название *</label>
                    <input id="title" v-model="form.title" type="text" required minlength="3" maxlength="255"
                        placeholder="Например: Уютная квартира в центре" />
                </div>

                <div class="form-group">
                    <label for="address">Адрес *</label>
                    <input id="address" v-model="form.address" type="text" required minlength="5" maxlength="255"
                        placeholder="Например: ул. Ленина, д. 10, кв. 5" />
                </div>

                <div class="form-group">
                    <label for="description">Описание</label>
                    <textarea id="description" v-model="form.description" rows="4" maxlength="5000"
                        placeholder="Опишите особенности объекта, состояние, преимущества..." />
                    <span class="char-count">{{ descriptionLength }}/5000</span>
                </div>

                <div v-if="propertiesStore.error" class="error-message">
                    {{ propertiesStore.error }}
                </div>

                <div class="modal-actions">
                    <button type="button" class="btn-cancel" @click="$emit('close')">
                        Отмена
                    </button>
                    <button type="submit" class="btn-submit" :disabled="propertiesStore.loading">
                        {{ propertiesStore.loading ? 'Создание...' : 'Создать объект' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { usePropertiesStore } from '../../stores/properties';
import { PROPERTY_TYPES } from '../../types/property';

const props = defineProps<{
    visible: boolean;
}>();

const emit = defineEmits<{
    close: [];
    created: [];
}>();

const propertiesStore = usePropertiesStore();

const form = reactive({
    property_type: '',
    title: '',
    address: '',
    description: '',
});

const descriptionLength = computed(() => form.description.length);

const resetForm = () => {
    form.property_type = '';
    form.title = '';
    form.address = '';
    form.description = '';
};

const handleSubmit = async () => {
    propertiesStore.clearError();

    const result = await propertiesStore.createProperty({
        property_type: form.property_type,
        title: form.title,
        address: form.address,
        description: form.description || undefined,
    });

    if (result) {
        resetForm();
        emit('created');
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
    animation: fadeIn 0.2s ease;
}

.modal-content {
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideUp 0.3s ease;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
    margin: 0;
    font-size: 1.25rem;
    color: #2d3748;
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #a0aec0;
    cursor: pointer;
    padding: 0.25rem;
    line-height: 1;
    transition: color 0.3s;
}

.modal-close:hover {
    color: #4a5568;
}

.modal-body {
    padding: 1.5rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #4a5568;
    font-size: 0.9rem;
}

input,
select,
textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: border-color 0.3s, box-shadow 0.3s;
    box-sizing: border-box;
}

input:focus,
select:focus,
textarea:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

select {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23a0aec0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 1.25rem;
    padding-right: 2.5rem;
}

textarea {
    resize: vertical;
    min-height: 100px;
}

.char-count {
    display: block;
    text-align: right;
    color: #a0aec0;
    font-size: 0.8rem;
    margin-top: 0.25rem;
}

.error-message {
    background: #fff5f5;
    color: #c53030;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.875rem;
}

.modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 2rem;
}

.btn-cancel,
.btn-submit {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-cancel {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    color: #4a5568;
}

.btn-cancel:hover {
    background: #edf2f7;
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

.btn-submit:disabled {
    opacity: 0.6;
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