<!-- components/properties/PropertyCard.vue -->
<template>
    <div class="property-card" @click="goToDetail">

        <!-- Фото / плейсхолдер -->
        <div class="card-image">
            <img v-if="property.image_url" :src="getImageUrl(property.image_url)" :alt="property.title" />
            <div v-else class="card-image-placeholder">
                <!-- Первая буква типа как декоративный акцент -->
                <span class="placeholder-letter">{{ propertyTypeLabel[0] }}</span>
            </div>

            <!-- Бейдж типа — стеклянный поверх фото -->
            <span class="type-badge">{{ propertyTypeLabel }}</span>
        </div>

        <!-- Тело -->
        <div class="card-body">
            <h3 class="card-title">{{ property.title }}</h3>
            <p class="card-address">
                <svg width="11" height="13" viewBox="0 0 11 13" fill="none">
                    <path
                        d="M5.5 1C3.015 1 1 3.015 1 5.5c0 3.375 4.5 7.5 4.5 7.5s4.5-4.125 4.5-7.5C10 3.015 7.985 1 5.5 1Z"
                        stroke="currentColor" stroke-width="1.2" />
                    <circle cx="5.5" cy="5.5" r="1.5" stroke="currentColor" stroke-width="1.2" />
                </svg>
                {{ property.address }}
            </p>
            <p v-if="property.description" class="card-description">{{ truncatedDescription }}</p>
        </div>

        <!-- Футер -->
        <div class="card-footer">
            <span class="card-arrow">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
                        stroke-linejoin="round" />
                </svg>
            </span>
        </div>

    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import type { PropertyResponse } from '../../types/property';
import { PROPERTY_TYPES } from '../../types/property';

const router = useRouter();
const props = defineProps<{ property: PropertyResponse }>();

const propertyTypeLabel = computed(() => {
    const t = PROPERTY_TYPES.find(t => t.value === props.property.property_type);
    return t ? t.label : props.property.property_type;
});

const truncatedDescription = computed(() => {
    if (!props.property.description) return '';
    return props.property.description.length > 90
        ? props.property.description.substring(0, 90) + '…'
        : props.property.description;
});

const getImageUrl = (url: string) =>
    url.startsWith('http') ? url : `http://localhost:8000${url}`;

const goToDetail = () =>
    router.push({ name: 'PropertyDetail', params: { id: props.property.id } });
</script>

<style scoped>
.property-card {
    /* Стеклянная карточка поверх blob-фона лейаута */
    background: rgba(255, 255, 255, 0.52);
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: var(--radius-lg);
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.70) inset, 0 6px 24px rgba(28, 26, 23, 0.07);
    transition: box-shadow var(--transition), transform var(--transition), border-color var(--transition);
    display: flex;
    flex-direction: column;
}

.property-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.80) inset, 0 16px 40px rgba(28, 26, 23, 0.12);
    border-color: rgba(255, 255, 255, 0.85);
}

/* ---- Фото ---- */
.card-image {
    position: relative;
    width: 100%;
    height: 172px;
    overflow: hidden;
    flex-shrink: 0;
}

.card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 400ms ease;
}

.property-card:hover .card-image img {
    transform: scale(1.04);
}

/* Плейсхолдер с градиентом из пастельной палитры */
.card-image-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg,
            rgba(196, 120, 138, 0.30) 0%,
            rgba(155, 137, 180, 0.25) 50%,
            rgba(196, 154, 120, 0.20) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}

.placeholder-letter {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: rgba(28, 26, 23, 0.12);
    font-family: var(--font-base);
    /* Небольшой сдвиг для визуального интереса */
    transform: rotate(-8deg);
}

/* Бейдж типа — стекло поверх фото */
.type-badge {
    position: absolute;
    top: var(--space-3);
    left: var(--space-3);
    padding: 3px var(--space-3);
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.90);
    border-radius: 20px;
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--color-dark);
    letter-spacing: 0.02em;
}

/* ---- Тело ---- */
.card-body {
    padding: var(--space-5) var(--space-5) var(--space-4);
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.card-title {
    font-size: var(--text-md);
    font-weight: 700;
    color: var(--color-dark);
    letter-spacing: -0.02em;
    line-height: 1.3;
}

.card-address {
    display: flex;
    align-items: flex-start;
    gap: var(--space-2);
    font-size: var(--text-sm);
    color: var(--color-dark-60);
    line-height: 1.4;
}

.card-address svg {
    flex-shrink: 0;
    margin-top: 2px;
    color: var(--color-dark-35);
}

.card-description {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
    line-height: 1.5;
    margin-top: var(--space-1);
}

/* ---- Футер ---- */
.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-3) var(--space-5);
    border-top: 1px solid rgba(28, 26, 23, 0.07);
}

.card-id {
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--color-dark-35);
    font-variant-numeric: tabular-nums;
}

.card-id::before {
    content: '# ';
}

.card-arrow {
    color: var(--color-dark-35);
    display: flex;
    align-items: center;
    transition: transform var(--transition), color var(--transition);
}

.property-card:hover .card-arrow {
    color: var(--color-emerald);
    transform: translateX(3px);
}
</style>