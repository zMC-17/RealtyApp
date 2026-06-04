<!-- components/requests/RequestCard.vue -->
<template>
    <div class="request-card" :class="`request-card--${request.status}`">
        <div class="request-card__header">
            <h4 class="request-title">{{ request.title }}</h4>
            <span class="request-status" :style="{ backgroundColor: statusColor }">
                {{ statusLabel }}
            </span>
        </div>

        <p class="request-message">{{ request.message }}</p>

        <div class="request-card__footer">
            <div class="request-meta">
                <span v-if="request.property_info?.title" class="meta-item">
                    🏠 {{ request.property_info.title }}
                </span>
                <span v-if="request.tenant_info?.name" class="meta-item">
                    👤 {{ request.tenant_info.name }}
                </span>
                <span v-if="request.owner_info?.name" class="meta-item">
                    👤 {{ request.owner_info.name }}
                </span>
            </div>

            <!-- Выпадающий список для владельца -->
            <select v-if="showActions && canChangeStatus" class="status-select" :value="request.status"
                @change="$emit('statusChange', request.id, ($event.target as HTMLSelectElement).value)">
                <option v-for="(label, status) in REQUEST_STATUS_LABELS" :key="status" :value="status">
                    {{ label }}
                </option>
            </select>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { RequestWithDetails } from '../../types/request';
import { REQUEST_STATUS_LABELS, REQUEST_STATUS_COLORS } from '../../types/request';

const props = defineProps<{
    request: RequestWithDetails;
    showActions: boolean;
}>();

defineEmits<{
    statusChange: [requestId: number, newStatus: string];
}>();

const statusLabel = computed(() => REQUEST_STATUS_LABELS[props.request.status] || props.request.status);
const statusColor = computed(() => REQUEST_STATUS_COLORS[props.request.status] || '#6b7280');
const canChangeStatus = computed(() => props.request.status !== 'completed' && props.request.status !== 'cancelled');
</script>

<style scoped>
.request-card {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    border-left: 4px solid #e5e7eb;
}

.request-card--open {
    border-left-color: #ef4444;
}

.request-card--in_progress {
    border-left-color: #f59e0b;
}

.request-card--completed {
    border-left-color: #10b981;
    opacity: 0.7;
}

.request-card--cancelled {
    border-left-color: #6b7280;
    opacity: 0.6;
}

.request-card__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.request-title {
    margin: 0;
    font-size: 1rem;
    color: #1f2937;
}

.request-status {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    color: white;
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
    flex-shrink: 0;
}

.request-message {
    margin: 0 0 0.75rem 0;
    color: #4b5563;
    font-size: 0.9rem;
    line-height: 1.5;
}

.request-card__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.request-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.meta-item {
    font-size: 0.8rem;
    color: #6b7280;
}

.status-select {
    padding: 0.35rem 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.8rem;
    background: white;
    cursor: pointer;
}
</style>