<!-- components/properties/CreatePropertyModal.vue -->
<template>
    <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-box">

            <div class="modal-header">
                <span class="modal-title">Добавить объект</span>
                <button class="modal-close" @click="$emit('close')">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5"
                            stroke-linecap="round" />
                    </svg>
                </button>
            </div>

            <form @submit.prevent="handleSubmit" class="modal-body">

                <div class="field">
                    <label class="field-label" for="propertyType">Тип недвижимости *</label>
                    <div class="select-wrap">
                        <select id="propertyType" class="field-input" v-model="form.property_type" required>
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
                    <label class="field-label" for="propTitle">Название *</label>
                    <input class="field-input" id="propTitle" v-model="form.title" type="text" required minlength="3"
                        maxlength="255" placeholder="Например: Уютная квартира в центре" />
                </div>

                <div class="field">
                    <label class="field-label" for="propAddress">Адрес *</label>
                    <input class="field-input" id="propAddress" v-model="form.address" type="text" required
                        minlength="5" maxlength="255" placeholder="ул. Ленина, д. 10, кв. 5" />
                </div>

                <div class="field">
                    <label class="field-label" for="propDescription">Описание</label>
                    <textarea class="field-input field-textarea" id="propDescription" v-model="form.description"
                        rows="4" maxlength="5000" placeholder="Особенности объекта, состояние, преимущества…" />
                    <span class="field-hint">{{ form.description.length }} / 5000</span>
                </div>

                <!-- Загрузка фото -->
                <div class="field">
                    <label class="field-label">Фото объекта</label>
                    <div class="upload-area" :class="{ 'upload-area--has-file': imagePreview }"
                        @click="triggerFileInput">
                        <input ref="fileInput" type="file" accept="image/jpeg,image/png,image/webp" hidden
                            @change="handleFileSelect" />

                        <div v-if="imagePreview" class="upload-preview">
                            <img :src="imagePreview" alt="Предпросмотр" />
                            <button type="button" class="upload-remove" @click.stop="removeFile">
                                <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                                    <path d="M1 1l8 8M9 1L1 9" stroke="white" stroke-width="1.5"
                                        stroke-linecap="round" />
                                </svg>
                            </button>
                        </div>

                        <div v-else class="upload-placeholder">
                            <div class="upload-icon">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                                    <path d="M3.5 13.5v2A1.5 1.5 0 0 0 5 17h10a1.5 1.5 0 0 0 1.5-1.5v-2"
                                        stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
                                    <path d="M10 3v9M7 6l3-3 3 3" stroke="currentColor" stroke-width="1.3"
                                        stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                            </div>
                            <span class="upload-text">Нажмите чтобы выбрать фото</span>
                            <span class="upload-hint">JPEG, PNG, WebP · до 5 МБ</span>
                        </div>
                    </div>
                    <span v-if="uploading" class="upload-status">
                        <span class="upload-status-dot"></span>
                        Загрузка фото…
                    </span>
                </div>

                <div v-if="propertiesStore.error" class="field-error-block">
                    {{ propertiesStore.error }}
                </div>

            </form>

            <div class="modal-footer">
                <button class="btn-cancel" type="button" @click="$emit('close')">Отмена</button>
                <button class="btn-confirm" type="button" :disabled="propertiesStore.loading || uploading"
                    @click="handleSubmit">
                    <span v-if="propertiesStore.loading || uploading" class="btn-spinner"></span>
                    {{ propertiesStore.loading ? 'Создание…' : uploading ? 'Загрузка…' : 'Создать объект' }}
                </button>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { usePropertiesStore } from '../../stores/properties';
import { PROPERTY_TYPES } from '../../types/property';
import api from '../../services/api';

defineProps<{ visible: boolean }>();
const emit = defineEmits<{ close: []; created: [] }>();

const propertiesStore = usePropertiesStore();
const fileInput = ref<HTMLInputElement>();
const selectedFile = ref<File | null>(null);
const imagePreview = ref('');
const uploading = ref(false);

const form = reactive({ property_type: '', title: '', address: '', description: '' });

const triggerFileInput = () => fileInput.value?.click();

const handleFileSelect = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    selectedFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
};

const removeFile = () => {
    selectedFile.value = null;
    imagePreview.value = '';
    if (fileInput.value) fileInput.value.value = '';
};

const resetForm = () => {
    form.property_type = ''; form.title = ''; form.address = ''; form.description = '';
    removeFile();
};

const uploadImage = async (): Promise<string | null> => {
    if (!selectedFile.value) return null;
    uploading.value = true;
    try {
        const fd = new FormData();
        fd.append('file', selectedFile.value);
        const { data } = await api.post('/uploads/property-image', fd, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return data.url;
    } catch { return null; }
    finally { uploading.value = false; }
};

const handleSubmit = async () => {
    propertiesStore.clearError();
    const imageUrl = await uploadImage();
    const result = await propertiesStore.createProperty({
        property_type: form.property_type,
        title: form.title,
        address: form.address,
        description: form.description || undefined,
        image_url: imageUrl || null,
    });
    if (result) { resetForm(); emit('created'); emit('close'); }
};
</script>

<style scoped>
/* ---- Оверлей ---- */
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

/* ---- Окно ---- */
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
    min-height: 96px;
}

/* Select — убираем нативную стрелку, добавляем свою */
.select-wrap {
    position: relative;
}

.field-input[type=""] select,
select.field-input {
    appearance: none;
    padding-right: var(--space-8);
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

.field-hint {
    font-size: var(--text-xs);
    color: var(--color-dark-35);
    text-align: right;
}

/* ---- Загрузка фото ---- */
.upload-area {
    border: 1.5px dashed rgba(28, 26, 23, 0.20);
    border-radius: var(--radius-md);
    padding: var(--space-6);
    text-align: center;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.40);
    transition: border-color var(--transition), background var(--transition);
}

.upload-area:hover,
.upload-area--has-file {
    border-color: rgba(26, 107, 74, 0.30);
    background: rgba(26, 107, 74, 0.03);
}

.upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-2);
}

.upload-icon {
    width: 40px;
    height: 40px;
    border-radius: var(--radius-md);
    background: rgba(28, 26, 23, 0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-dark-35);
    margin-bottom: var(--space-1);
}

.upload-text {
    font-size: var(--text-sm);
    font-weight: 500;
    color: var(--color-dark-60);
}

.upload-hint {
    font-size: var(--text-xs);
    color: var(--color-dark-35);
}

.upload-preview {
    position: relative;
    display: inline-block;
}

.upload-preview img {
    max-height: 180px;
    border-radius: var(--radius-md);
    display: block;
}

.upload-remove {
    position: absolute;
    top: -8px;
    right: -8px;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--color-danger);
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background var(--transition);
}

.upload-remove:hover {
    background: #9b2a2a;
}

.upload-status {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-xs);
    color: var(--color-dark-60);
    margin-top: var(--space-1);
}

.upload-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--color-emerald);
    animation: pulse-dot 1.2s ease-in-out infinite;
}

@keyframes pulse-dot {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.3;
    }
}

/* ---- Ошибка ---- */
.field-error-block {
    padding: var(--space-3) var(--space-4);
    background: var(--color-danger-bg);
    border: 1px solid rgba(185, 64, 64, 0.18);
    border-radius: var(--radius-md);
    color: var(--color-danger);
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
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
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