<!-- components/properties/EmptyState.vue -->
<template>
    <div class="empty-state">
        <div class="empty-state__icon">🏠</div>
        <h2 class="empty-state__title">У вас пока нет объектов</h2>
        <p class="empty-state__description">
            Добавьте свой первый объект недвижимости, чтобы начать управление арендой
        </p>
        <button class="empty-state__button" @click="$emit('create')">
            Добавить объект
        </button>
    </div>
</template>

<script setup lang="ts">
defineEmits<{
    create: [];
}>();
</script>

<style scoped>
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
}

.empty-state__icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    opacity: 0.6;
}

.empty-state__title {
    font-size: 1.5rem;
    color: #2d3748;
    margin: 0 0 0.5rem 0;
}

.empty-state__description {
    color: #a0aec0;
    margin: 0 0 2rem 0;
    max-width: 400px;
    line-height: 1.5;
}

.empty-state__button {
    padding: 0.875rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.empty-state__button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>