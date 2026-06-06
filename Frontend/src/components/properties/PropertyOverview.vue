<!-- components/properties/PropertyOverview.vue -->
<template>
    <div class="property-overview">
        <div class="info-card">
            <div class="info-row">
                <span class="info-label">Тип недвижимости</span>
                <span class="info-value">{{ propertyTypeLabel }}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Адрес</span>
                <span class="info-value">{{ property.address }}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Описание</span>
                <span class="info-value">{{ property.description || 'Нет описания' }}</span>
            </div>
        </div>

        <div class="actions">
            <button class="btn-edit" @click="$emit('edit')">
                ✏️ Редактировать
            </button>
            <button class="btn-delete" @click="$emit('delete')">
                🗑️ Удалить
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PropertyResponse } from '../../types/property';
import { PROPERTY_TYPES } from '../../types/property';

const props = defineProps<{ property: PropertyResponse }>();
defineEmits(['edit', 'delete']);

const propertyTypeLabel = computed(() => {
    const type = PROPERTY_TYPES.find(t => t.value === props.property.property_type);
    return type ? type.label : props.property.property_type;
});
</script>

<style scoped>
.property-overview {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.info-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.info-row {
    display: flex;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f3f4f6;
}

.info-row:last-child {
    border-bottom: none;
}

.info-label {
    width: 200px;
    color: #6b7280;
    font-weight: 500;
    flex-shrink: 0;
}

.info-value {
    color: #1f2937;
}

.actions {
    display: flex;
    gap: 1rem;
}

.btn-edit,
.btn-delete {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 0.95rem;
    cursor: pointer;
    transition: transform 0.2s;
}

.btn-edit {
    background: #667eea;
    color: white;
}

.btn-delete {
    background: #ef4444;
    color: white;
}

.btn-edit:hover,
.btn-delete:hover {
    transform: translateY(-2px);
}
</style>