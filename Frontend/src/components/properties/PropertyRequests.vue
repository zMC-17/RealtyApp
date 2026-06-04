<!-- components/properties/PropertyRequests.vue -->
<template>
    <div class="property-requests">
        <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Загрузка заявок...</p>
        </div>

        <div v-else-if="sortedRequests.length === 0" class="empty-state">
            <p>Заявок пока нет</p>
        </div>

        <div v-else class="requests-list">
            <div v-for="request in sortedRequests" :key="request.id" class="request-card"
                :class="`request-card--${request.status}`">
                <div class="request-header">
                    <h4 class="request-title">{{ request.title || 'Без названия' }}</h4>
                    <span class="request-status-badge" :style="{ backgroundColor: statusColor(request.status) }">
                        {{ statusLabel(request.status) }}
                    </span>
                </div>

                <p class="request-message">{{ request.message }}</p>

                <div class="request-footer">
                    <span class="request-id">#{{ request.id }}</span>

                    <!-- Выпадающий список статусов (как на общей странице) -->
                    <select v-if="canChangeStatus(request.status)" class="status-select" :value="request.status"
                        @change="updateStatus(request.id, ($event.target as HTMLSelectElement).value)">
                        <option value="open">Открыта</option>
                        <option value="in_progress">В работе</option>
                        <option value="completed">Выполнена</option>
                        <option value="cancelled">Отменена</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { requestsService } from '../../services/requests';
import { REQUEST_STATUS_LABELS, REQUEST_STATUS_COLORS } from '../../types/request';
import type { RequestResponse, RequestStatus } from '../../types/request';

const props = defineProps<{ contractId: number }>();

const requests = ref<RequestResponse[]>([]);
const loading = ref(true);

// Открытые и в работе сверху, выполненные и отменённые снизу
const sortedRequests = computed(() => {
    const active = requests.value.filter(r => r.status === 'open' || r.status === 'in_progress');
    const closed = requests.value.filter(r => r.status === 'completed' || r.status === 'cancelled');
    return [...active, ...closed];
});

const canChangeStatus = (status: string) => {
    return status !== 'completed' && status !== 'cancelled';
};

const statusLabel = (status: string) => {
    return REQUEST_STATUS_LABELS[status as RequestStatus] || status;
};

const statusColor = (status: string) => {
    return REQUEST_STATUS_COLORS[status as RequestStatus] || '#6b7280';
};

const loadRequests = async () => {
    loading.value = true;
    try {
        requests.value = await requestsService.getContractRequests(props.contractId);
    } catch (err) {
        console.error('Ошибка загрузки заявок:', err);
    } finally {
        loading.value = false;
    }
};

const updateStatus = async (requestId: number, newStatus: string) => {
    await requestsService.updateRequestStatus(requestId, newStatus);
    await loadRequests();
};

onMounted(loadRequests);
</script>

<style scoped>
.property-requests {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.requests-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.request-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
    background: #f9fafb;
}

.request-card--cancelled {
    border-left-color: #6b7280;
    opacity: 0.6;
    background: #f9fafb;
}

.request-header {
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

.request-status-badge {
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

.request-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.request-id {
    font-size: 0.75rem;
    color: #9ca3af;
}

.status-select {
    padding: 0.35rem 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.8rem;
    background: white;
    cursor: pointer;
    color: #374151;
}

.status-select:focus {
    outline: none;
    border-color: #667eea;
}

.loading-state,
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    color: #6b7280;
}

.spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e5e7eb;
    border-top: 3px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 0.75rem;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>