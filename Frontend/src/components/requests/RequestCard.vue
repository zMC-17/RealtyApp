<!-- components/requests/RequestCard.vue -->
<template>
    <div class="request-card" :class="{
        'request-card--open': request.status === 'open',
        'request-card--in-progress': request.status === 'in_progress',
        'request-card--completed': request.status === 'completed',
        'request-card--cancelled': request.status === 'cancelled',
    }">
        <!-- Левая полоска -->
        <div class="card-accent"></div>

        <div class="card-inner">
            <!-- Шапка: заголовок + статус-бейдж -->
            <div class="card-header">
                <h4 class="card-title">{{ request.title }}</h4>
                <span class="status-badge" :class="`status-badge--${request.status}`">
                    {{ statusLabel }}
                </span>
            </div>

            <!-- Текст обращения -->
            <p class="card-message">{{ request.message }}</p>

            <!-- Футер: чипы + смена статуса -->
            <div class="card-footer">
                <div class="card-chips">
                    <span v-if="request.property_info?.title" class="chip">
                        <svg width="10" height="11" viewBox="0 0 10 11" fill="none">
                            <path d="M1 5L5 1.5 9 5v5H7V7H3v3H1V5Z" stroke="currentColor" stroke-width="1.1"
                                stroke-linejoin="round" />
                        </svg>
                        {{ request.property_info.title }}
                    </span>
                    <span v-if="request.tenant_info?.name" class="chip">
                        <svg width="10" height="11" viewBox="0 0 10 11" fill="none">
                            <circle cx="5" cy="3.5" r="2" stroke="currentColor" stroke-width="1.1" />
                            <path d="M1 10c0-2.21 1.79-4 4-4s4 1.79 4 4" stroke="currentColor" stroke-width="1.1"
                                stroke-linecap="round" />
                        </svg>
                        {{ request.tenant_info.name }}
                    </span>
                    <span v-if="request.owner_info?.name" class="chip">
                        <svg width="10" height="11" viewBox="0 0 10 11" fill="none">
                            <circle cx="5" cy="3.5" r="2" stroke="currentColor" stroke-width="1.1" />
                            <path d="M1 10c0-2.21 1.79-4 4-4s4 1.79 4 4" stroke="currentColor" stroke-width="1.1"
                                stroke-linecap="round" />
                        </svg>
                        {{ request.owner_info.name }}
                    </span>
                </div>

                <!-- Смена статуса — только владелец, только активные -->
                <div v-if="showActions && canChangeStatus" class="status-change">
                    <label class="status-change-label">Статус</label>
                    <div class="select-wrap">
                        <select class="status-select" :value="request.status"
                            @change="$emit('statusChange', request.id, ($event.target as HTMLSelectElement).value)">
                            <option v-for="(label, st) in REQUEST_STATUS_LABELS" :key="st" :value="st">
                                {{ label }}
                            </option>
                        </select>
                        <svg class="select-arrow" width="10" height="10" viewBox="0 0 10 10" fill="none">
                            <path d="M2 3.5l3 3 3-3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"
                                stroke-linejoin="round" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { RequestWithDetails } from '../../types/request';
import { REQUEST_STATUS_LABELS } from '../../types/request';

const props = defineProps<{ request: RequestWithDetails; showActions: boolean }>();
defineEmits<{ statusChange: [id: number, status: string] }>();

const statusLabel = computed(() => REQUEST_STATUS_LABELS[props.request.status] || props.request.status);
const canChangeStatus = computed(() => !['completed', 'cancelled'].includes(props.request.status));
</script>

<style scoped>
.request-card {
    display: flex;
    background: rgba(255, 255, 255, 0.50);
    backdrop-filter: blur(16px) saturate(130%);
    -webkit-backdrop-filter: blur(16px) saturate(130%);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.65) inset, 0 2px 8px rgba(28, 26, 23, 0.05);
    transition: box-shadow var(--transition), border-color var(--transition);
}

.request-card:hover {
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.80) inset, 0 6px 20px rgba(28, 26, 23, 0.09);
    border-color: rgba(255, 255, 255, 0.82);
}

/* Затухание закрытых/отменённых */
.request-card--completed,
.request-card--cancelled {
    opacity: 0.65;
}

/* ---- Полоска слева ---- */
.card-accent {
    width: 3px;
    flex-shrink: 0;
    border-radius: 0;
    background: transparent;
    transition: background var(--transition);
}

.request-card--open .card-accent {
    background: var(--color-danger);
}

.request-card--in-progress .card-accent {
    background: var(--color-warning);
}

.request-card--completed .card-accent {
    background: var(--color-emerald);
}

.request-card--cancelled .card-accent {
    background: var(--color-neutral);
}

/* ---- Внутренний контент ---- */
.card-inner {
    flex: 1;
    min-width: 0;
    padding: var(--space-4) var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

/* ---- Шапка ---- */
.card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-4);
}

.card-title {
    font-size: var(--text-base);
    font-weight: 700;
    color: var(--color-dark);
    letter-spacing: -0.01em;
    line-height: 1.3;
    margin: 0;
}

/* ---- Статус-бейдж ---- */
.status-badge {
    display: inline-flex;
    align-items: center;
    padding: 3px var(--space-3);
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    white-space: nowrap;
    flex-shrink: 0;
}

.status-badge--open {
    background: var(--color-danger-bg);
    color: var(--color-danger);
}

.status-badge--in_progress {
    background: var(--color-warning-bg);
    color: var(--color-warning);
}

.status-badge--completed {
    background: var(--color-success-bg);
    color: var(--color-success);
}

.status-badge--cancelled {
    background: var(--color-neutral-bg);
    color: var(--color-neutral);
}

/* ---- Текст ---- */
.card-message {
    font-size: var(--text-sm);
    color: var(--color-dark-60);
    line-height: 1.6;
    margin: 0;
}

/* ---- Футер ---- */
.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-4);
    flex-wrap: wrap;
}

/* Чипы */
.card-chips {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: var(--text-xs);
    font-weight: 500;
    color: var(--color-dark-35);
    background: rgba(28, 26, 23, 0.06);
    border-radius: var(--radius-sm);
    padding: 2px var(--space-2);
}

.chip svg {
    flex-shrink: 0;
    color: var(--color-dark-35);
}

/* Смена статуса */
.status-change {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    flex-shrink: 0;
}

.status-change-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--color-dark-35);
}

.select-wrap {
    position: relative;
}

.status-select {
    appearance: none;
    padding: var(--space-2) var(--space-6) var(--space-2) var(--space-3);
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(28, 26, 23, 0.12);
    border-radius: var(--radius-md);
    color: var(--color-dark);
    font-family: var(--font-base);
    font-size: var(--text-xs);
    font-weight: 600;
    cursor: pointer;
    transition: border-color var(--transition), background var(--transition);
}

.status-select:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.90);
    border-color: var(--color-emerald-20);
    box-shadow: 0 0 0 3px var(--color-emerald-08);
}

.select-arrow {
    position: absolute;
    right: var(--space-2);
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-dark-35);
    pointer-events: none;
}
</style>