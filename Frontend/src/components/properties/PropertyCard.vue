<template>
    <div class="property-card" @click="goToDetail">
        <!-- Фото -->
        <div class="property-card__image">
            <img v-if="property.image_url" :src="getImageUrl(property.image_url)" :alt="property.title" />
            <div v-else class="property-card__image-placeholder">
                <span>{{ propertyTypeLabel[0] }}</span>
            </div>
            <div class="property-type-badge">
                {{ propertyTypeLabel }}
            </div>
        </div>

        <div class="property-card__body">
            <h3 class="property-card__title">{{ property.title }}</h3>
            <p class="property-card__address">
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

const propertyTypeLabel = computed(() => {
    const type = PROPERTY_TYPES.find(t => t.value === props.property.property_type);
    return type ? type.label : props.property.property_type;
});

const truncatedDescription = computed(() => {
    if (!props.property.description) return '';
    return props.property.description.length > 80
        ? props.property.description.substring(0, 80) + '...'
        : props.property.description;
});

const getImageUrl = (url: string) => {
    if (url.startsWith('http')) return url;
    return `http://localhost:8000${url}`;
};

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

/* Фото */
.property-card__image {
    position: relative;
    width: 100%;
    height: 180px;
    overflow: hidden;
}

.property-card__image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.property-card__image-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}

.property-card__image-placeholder span {
    font-size: 3rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.4);
}

.property-type-badge {
    position: absolute;
    top: 0.75rem;
    left: 0.75rem;
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: rgba(255, 255, 255, 0.9);
    color: #374151;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.property-card__body {
    padding: 1rem 1.25rem;
}

.property-card__title {
    margin: 0 0 0.5rem 0;
    font-size: 1.15rem;
    color: #2d3748;
    font-weight: 600;
}

.property-card__address {
    margin: 0 0 0.5rem 0;
    color: #718096;
    font-size: 0.9rem;
}

.property-card__description {
    margin: 0;
    color: #a0aec0;
    font-size: 0.85rem;
    line-height: 1.4;
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