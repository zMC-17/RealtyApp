<!-- components/properties/PropertyCard.vue -->
<template>
    <div class="property-card" @click="goToDetail">
        <div class="property-card__header">
            <div class="property-type-badge">
                {{ propertyTypeLabel }}
            </div>
        </div>

        <div class="property-card__body">
            <h3 class="property-card__title">{{ property.title }}</h3>
            <p class="property-card__address">
                <span class="address-icon">📍</span>
                {{ property.address }}
            </p>
            <p v-if="property.description" class="property-card__description">
                {{ truncatedDescription }}
            </p>
        </div>

        <div class="property-card__footer">
            <span class="property-card__id">ID: {{ property.id }}</span>
            <span class="property-card__arrow">→</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import type { PropertyResponse } from '../../types/property';
import { PROPERTY_TYPES } from '../../types/property';

const router = useRouter();

const props = defineProps<{
    property: PropertyResponse;
}>();

defineEmits<{
    click: [id: number];
}>();

const propertyTypeLabel = computed(() => {
    const type = PROPERTY_TYPES.find(t => t.value === props.property.property_type);
    return type ? type.label : props.property.property_type;
});

const truncatedDescription = computed(() => {
    if (!props.property.description) return '';
    return props.property.description.length > 100
        ? props.property.description.substring(0, 100) + '...'
        : props.property.description;
});

const goToDetail = () => {
    router.push({ name: 'PropertyDetail', params: { id: props.property.id } });
};
</script>

<style scoped>
.property-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    overflow: hidden;
}

.property-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.property-card__header {
    padding: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.property-type-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
}

.property-card__body {
    padding: 1.25rem;
}

.property-card__title {
    margin: 0 0 0.75rem 0;
    font-size: 1.25rem;
    color: #2d3748;
    font-weight: 600;
}

.property-card__address {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 0.5rem 0;
    color: #718096;
    font-size: 0.95rem;
}

.address-icon {
    flex-shrink: 0;
}

.property-card__description {
    margin: 0;
    color: #a0aec0;
    font-size: 0.875rem;
    line-height: 1.5;
}

.property-card__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1.25rem;
    border-top: 1px solid #e2e8f0;
}

.property-card__id {
    color: #a0aec0;
    font-size: 0.75rem;
}

.property-card__arrow {
    color: #667eea;
    font-size: 1.25rem;
    transition: transform 0.3s ease;
}

.property-card:hover .property-card__arrow {
    transform: translateX(4px);
}
</style>