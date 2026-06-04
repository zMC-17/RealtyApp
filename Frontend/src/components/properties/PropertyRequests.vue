<!-- components/properties/PropertyRequests.vue -->
<template>
    <div class="property-requests">
        <div v-if="loading" class="loading">Загрузка заявок...</div>

        <div v-else-if="sortedRequests.length === 0" class="empty">
            <p>Заявок пока нет</p>
        </div>

        <div v-else class="requests-list">
            <div v-for="request in sortedRequests" :key="request.id" class="request-card"
                :class="{ completed: request.status === 'completed' }">
                <div class="request-header">
                    <span class="request-status" :class="request.status">
                        {{ request.status === 'open' ? '🔴 Открыта' : '✅ Выполнена' }}
                    </span>
                    <span class="request-id">#{{ request.id }}</span>
                </div>

                <p class="request-message">{{ request.message }}</p>

                <button v-if="request.status === 'open'" class="btn-complete" @click="completeRequest(request.id)">
                    Отметить выполненной
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { requestsService } from '../../services/requests';
import type { RequestResponse } from '../../types/request';

const props = defineProps<{ contractId: number }>();

const requests = ref<RequestResponse[]>([]);
const loading = ref(true);

// Открытые сверху, выполненные снизу
const sortedRequests = computed(() => {
    const open = requests.value.filter(r => r.status === 'open');
    const completed = requests.value.filter(r => r.status === 'completed');
    return [...open, ...completed];
});

const loadRequests = async () => {
    loading.value = true;
    requests.value = await requestsService.getContractRequests(props.contractId);
    loading.value = false;
};

const completeRequest = async (requestId: number) => {
    await requestsService.updateRequest(requestId, { status: 'completed' });
    await loadRequests();
};

onMounted(loadRequests);
</script>

<style scoped>
.requests-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.request-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.request-card.completed {
    opacity: 0.7;
    background: #f9fafb;
}

.request-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.75rem;
}

.btn-complete {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #10b981;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}
</style>