<!-- components/properties/PropertyRequests.vue -->
<template>
    <div class="property-requests">

        <div v-if="loading" class="loader-wrap">
            <div class="loader-line"></div>
            <p class="loader-label">Загрузка заявок…</p>
        </div>

        <div v-else-if="sortedRequests.length === 0" class="empty-state">
            <div class="empty-icon-box">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M17 3H3a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h4l3 3 3-3h4a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1Z"
                        stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" />
                    <path d="M6 8h8M6 12h5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
                </svg>
            </div>
            <p class="empty-title">Заявок пока нет</p>
            <p class="empty-text">Заявки от арендатора появятся здесь</p>
        </div>

        <div v-else class="requests-list">
            <RequestCard v-for="request in sortedRequests" :key="request.id" :request="request" :show-actions="true"
                @status-change="updateStatus" />
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { requestsService } from '../../services/requests';
import type { RequestResponse } from '../../types/request';
import RequestCard from '../requests/RequestCard.vue';

const props = defineProps<{ contractId: number }>();

const requests = ref<RequestResponse[]>([]);
const loading = ref(true);

const sortedRequests = computed(() => {
    const active = requests.value.filter(r => ['open', 'in_progress'].includes(r.status));
    const closed = requests.value.filter(r => ['completed', 'cancelled'].includes(r.status));
    return [...active, ...closed];
});

const loadRequests = async () => {
    loading.value = true;
    try { requests.value = await requestsService.getContractRequests(props.contractId); }
    catch (err) { console.error(err); }
    finally { loading.value = false; }
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
    gap: var(--space-3);
}

.loader-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-12);
}

.loader-line {
    width: 120px;
    height: 2px;
    background: rgba(28, 26, 23, 0.10);
    border-radius: 1px;
    overflow: hidden;
    position: relative;
}

.loader-line::after {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--color-emerald);
    animation: loader 1.4s ease-in-out infinite;
}

@keyframes loader {
    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(200%);
    }
}

.loader-label {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-12) var(--space-8);
    text-align: center;
}

.empty-icon-box {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-lg);
    background: rgba(255, 255, 255, 0.52);
    border: 1px solid rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--space-2);
    color: var(--color-dark-35);
}

.empty-title {
    font-size: var(--text-md);
    font-weight: 700;
    color: var(--color-dark);
    letter-spacing: -0.02em;
}

.empty-text {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
}

.requests-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}
</style>