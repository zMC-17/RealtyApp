    <!-- components/properties/EditPropertyModal.vue -->
    <template>
        <div class="modal-overlay" @click.self="$emit('close')">
            <div class="modal-box">

                <div class="modal-header">
                    <span class="modal-title">Редактировать объект</span>
                    <button class="modal-close" @click="$emit('close')">
                        <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                            <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5"
                                stroke-linecap="round" />
                        </svg>
                    </button>
                </div>

                <form @submit.prevent="handleSubmit" class="modal-body">

                    <div class="field">
                        <label class="field-label" for="editPropertyType">Тип недвижимости *</label>
                        <div class="select-wrap">
                            <select class="field-input" id="editPropertyType" v-model="form.property_type" required
                                :disabled="loading">
                                <option value="" disabled>Выберите тип</option>
                                <option v-for="type in PROPERTY_TYPES" :key="type.value" :value="type.value">
                                    {{ type.label }}
                                </option>
                            </select>
                            <svg class="select-arrow" width="12" height="12" viewBox="0 0 12 12" fill="none">
                                <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
                                    stroke-linejoin="round" />
                            </svg>
                        </div>
                    </div>

                    <div class="field">
                        <label class="field-label" for="editTitle">Название *</label>
                        <input class="field-input" id="editTitle" v-model="form.title" type="text" required minlength="3"
                            maxlength="255" :disabled="loading" />
                    </div>

                    <div class="field">
                        <label class="field-label" for="editAddress">Адрес *</label>
                        <input class="field-input" id="editAddress" v-model="form.address" type="text" required
                            minlength="5" maxlength="255" :disabled="loading" />
                    </div>

                    <div class="field">
                        <label class="field-label" for="editDescription">Описание</label>
                        <textarea class="field-input field-textarea" id="editDescription" v-model="form.description"
                            rows="4" maxlength="5000" :disabled="loading" placeholder="Опишите особенности объекта…" />
                        <span class="field-hint">{{ form.description.length }} / 5000</span>
                    </div>

                    <div v-if="error" class="notice notice--danger">{{ error }}</div>

                </form>

                <div class="modal-footer">
                    <button class="btn-cancel" type="button" @click="$emit('close')" :disabled="loading">
                        Отмена
                    </button>
                    <button class="btn-confirm" type="button" :disabled="loading" @click="handleSubmit">
                        <span v-if="loading" class="btn-spinner"></span>
                        {{ loading ? 'Сохранение…' : 'Сохранить изменения' }}
                    </button>
                </div>

            </div>
        </div>
    </template>

    <script setup lang="ts">
    import { reactive, ref } from 'vue';
    import { propertiesService } from '../../services/properties';
    import { PROPERTY_TYPES } from '../../types/property';
    import type { PropertyResponse, PropertyCreate } from '../../types/property';

    const props = defineProps<{ property: PropertyResponse }>();
    const emit = defineEmits<{ close: []; updated: [property: PropertyResponse] }>();

    const loading = ref(false);
    const error = ref('');

    const form = reactive<PropertyCreate>({
        property_type: props.property.property_type,
        title: props.property.title,
        address: props.property.address,
        description: props.property.description || '',
        image_url: props.property.image_url
    });

    const handleSubmit = async () => {
        loading.value = true; error.value = '';
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
        max-width: 500px;
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

    .field-input:focus {
        outline: none;
        background: rgba(255, 255, 255, 0.90);
        border-color: var(--color-emerald-20);
        box-shadow: 0 0 0 3px var(--color-emerald-08);
    }

    .field-input:disabled {
        opacity: 0.50;
        cursor: not-allowed;
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

    .select-wrap {
        position: relative;
    }

    select.field-input {
        appearance: none;
        padding-right: var(--space-8);
        cursor: pointer;
    }

    .select-arrow {
        position: absolute;
        right: var(--space-4);
        top: 50%;
        transform: translateY(-50%);
        color: var(--color-dark-35);
        pointer-events: none;
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
    }

    .btn-confirm:hover:not(:disabled) {
        background: #2d2b27;
        box-shadow: 0 4px 16px rgba(28, 26, 23, 0.20);
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