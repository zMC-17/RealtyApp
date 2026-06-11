<!-- components/properties/PropertyOverview.vue -->
<template>
    <div class="overview">

        <!-- Фото если есть -->
        <div v-if="property.image_url" class="overview-image">
            <img :src="getImageUrl(property.image_url)" :alt="property.title" />
        </div>

        <!-- Информационная панель -->
        <div class="info-panel">
            <div class="info-row">
                <span class="info-label">Тип</span>
                <span class="info-value">{{ propertyTypeLabel }}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Адрес</span>
                <span class="info-value">{{ property.address }}</span>
            </div>
            <div class="info-row" v-if="property.description">
                <span class="info-label">Описание</span>
                <span class="info-value info-value--description">{{ property.description }}</span>
            </div>
        </div>

        <!-- Действия -->
        <div class="actions">
            <button class="btn-edit" @click="$emit('edit')">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M9.5 2.5l2 2L4 12H2v-2L9.5 2.5Z" stroke="currentColor" stroke-width="1.3"
                        stroke-linejoin="round" />
                    <path d="M8 4l2 2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
                </svg>
                Редактировать
            </button>
            <button class="btn-delete" @click="$emit('delete')">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M2 4h10M5 4V2.5h4V4M5.5 6.5v4M8.5 6.5v4M3 4l.75 7.5h6.5L11 4" stroke="currentColor"
                        stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                Удалить объект
            </button>
        </div>

    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PropertyResponse } from '../../types/property';
import { PROPERTY_TYPES } from '../../types/property';

const props = defineProps<{ property: PropertyResponse }>();
defineEmits<{ edit: []; delete: [] }>();

const propertyTypeLabel = computed(() => {
    const t = PROPERTY_TYPES.find(t => t.value === props.property.property_type);
    return t ? t.label : props.property.property_type;
});

const getImageUrl = (url: string) =>
    url.startsWith('http') ? url : `http://localhost:8000${url}`;
</script>

<style scoped>
.overview {
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
}

/* ---- Фото ---- */
.overview-image {
    width: 100%;
    max-height: 350px;
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.65);
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.70) inset, 0 8px 24px rgba(28, 26, 23, 0.08);
}

.overview-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* ---- Информационная панель ---- */
.info-panel {
    background: rgba(255, 255, 255, 0.52);
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.70) inset, 0 4px 16px rgba(28, 26, 23, 0.06);
}

.info-row {
    display: flex;
    align-items: baseline;
    gap: var(--space-6);
    padding: var(--space-4) var(--space-6);
    border-bottom: 1px solid rgba(28, 26, 23, 0.07);
}

.info-row:last-child {
    border-bottom: none;
}

.info-label {
    width: 120px;
    flex-shrink: 0;
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-dark-35);
}

.info-value {
    font-size: var(--text-sm);
    font-weight: 500;
    color: var(--color-dark);
    line-height: 1.5;
}

.info-value--description {
    color: var(--color-dark-60);
    font-weight: 400;
}

/* ---- Действия ---- */
.actions {
    display: flex;
    gap: var(--space-3);
}

.btn-edit {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-5);
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.70);
    border-radius: var(--radius-md);
    color: var(--color-dark);
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition);
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.65) inset;
}

.btn-edit:hover {
    background: rgba(255, 255, 255, 0.75);
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.80) inset, 0 4px 14px rgba(28, 26, 23, 0.10);
    transform: translateY(-1px);
}

.btn-delete {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-5);
    background: var(--color-danger-bg);
    border: 1px solid rgba(185, 64, 64, 0.20);
    border-radius: var(--radius-md);
    color: var(--color-danger);
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition);
}

.btn-delete:hover {
    background: rgba(185, 64, 64, 0.14);
    box-shadow: 0 4px 14px rgba(185, 64, 64, 0.15);
    transform: translateY(-1px);
}

.btn-delete:active {
    transform: translateY(0);
}
</style>