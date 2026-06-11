<!-- components/properties/EmptyState.vue -->
<template>
    <div class="empty-state">

        <div class="empty-icon-box">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <path d="M4 13L14 4l10 9v12a1.5 1.5 0 0 1-1.5 1.5h-5V18h-7v8.5H4.5A1.5 1.5 0 0 1 3 25V13Z"
                    stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" />
            </svg>
        </div>

        <h2 class="empty-title">У вас пока нет объектов</h2>
        <p class="empty-text">
            Добавьте первый объект недвижимости, чтобы начать управление арендой
        </p>

        <button class="btn-dark" @click="$emit('create')">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            </svg>
            Добавить объект
        </button>

    </div>
</template>

<script setup lang="ts">
defineEmits<{ create: [] }>();
</script>

<style scoped>
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-16) var(--space-8);
    text-align: center;
}

.empty-icon-box {
    width: 72px;
    height: 72px;
    border-radius: var(--radius-xl);
    background: rgba(255, 255, 255, 0.52);
    backdrop-filter: blur(16px) saturate(130%);
    -webkit-backdrop-filter: blur(16px) saturate(130%);
    border: 1px solid rgba(255, 255, 255, 0.70);
    box-shadow: 0 2px 0 rgba(255, 255, 255, 0.70) inset, 0 8px 24px rgba(28, 26, 23, 0.07);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-dark-35);
    margin-bottom: var(--space-4);
}

.empty-title {
    font-size: var(--text-xl);
    font-weight: 800;
    color: var(--color-dark);
    letter-spacing: -0.03em;
}

.empty-text {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
    max-width: 320px;
    line-height: 1.6;
    margin-bottom: var(--space-2);
}

.btn-dark {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-6);
    background: var(--color-dark);
    color: var(--color-bg);
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition);
}

.btn-dark:hover {
    background: #2d2b27;
    box-shadow: 0 4px 16px rgba(28, 26, 23, 0.22);
    transform: translateY(-1px);
}

.btn-dark:active {
    transform: translateY(0);
}
</style>