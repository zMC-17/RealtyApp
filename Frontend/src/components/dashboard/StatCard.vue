<!-- components/dashboard/StatCard.vue -->
<template>
    <div class="stat-card" :style="{ borderTopColor: color }">
        <div class="stat-card__icon" :style="{ color }">
            {{ icon }}
        </div>
        <div class="stat-card__content">
            <span class="stat-card__label">{{ label }}</span>
            <strong class="stat-card__value" :style="{ color }">{{ value }}</strong>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    icon: string;
    label: string;
    value: string | number;
    color: string;
}>();
</script>

<style scoped>
.stat-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    background: white;
    border-radius: 12px;
    border-top: 4px solid #667eea;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
}

.stat-card__icon {
    font-size: 2rem;
    flex-shrink: 0;
}

.stat-card__label {
    display: block;
    font-size: 0.8rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stat-card__value {
    font-size: 1.5rem;
    font-weight: 700;
}
</style>