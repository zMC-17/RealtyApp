<!-- pages/landlord/requests.vue -->
<template>
  <div class="landlord-requests">
    <div class="page-header">
      <h1>Заявки от арендаторов</h1>
      <button class="refresh-btn" @click="loadRequests" :disabled="loading">
        🔄 Обновить
      </button>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка заявок...</p>
    </div>

    <div v-else-if="requests.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <h2>Заявок пока нет</h2>
      <p>Когда арендаторы создадут заявки, они появятся здесь</p>
    </div>

    <template v-else>
      <!-- Активные (сгруппированы по объектам) -->
      <section v-if="activeRequests.length > 0" class="section">
        <h2 class="section-title section-title--active">
          <span>📋</span> Активные
          <span class="count-badge count-badge--active">{{ activeRequests.length }}</span>
        </h2>

        <div v-for="group in groupedActiveRequests" :key="group.propertyId" class="property-group">
          <h3 class="group-title">
            <span>🏠</span>
            {{ group.propertyTitle }}
            <span class="group-address">{{ group.propertyAddress }}</span>
          </h3>
          <div class="requests-list">
            <RequestCard v-for="req in group.requests" :key="req.id" :request="req" :show-actions="true"
              @status-change="handleStatusChange" />
          </div>
        </div>
      </section>

      <!-- Завершённые -->
      <section v-if="completedRequests.length > 0" class="section">
        <button class="collapse-btn" @click="showCompleted = !showCompleted">
          <span>{{ showCompleted ? '✅' : '▶️' }}</span>
          Завершённые
          <span class="count-badge count-badge--completed">{{ completedRequests.length }}</span>
        </button>
        <div v-if="showCompleted" class="requests-list">
          <RequestCard v-for="req in completedRequests" :key="req.id" :request="req" :show-actions="true"
            @status-change="handleStatusChange" />
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { requestsService } from '../../services/requests';
import type { RequestWithDetails } from '../../types/request';
import RequestCard from '../../components/requests/RequestCard.vue';

const requests = ref<RequestWithDetails[]>([]);
const loading = ref(true);
const showCompleted = ref(false);

const activeRequests = computed(() =>
  requests.value.filter(r => r.status === 'open' || r.status === 'in_progress')
);

const completedRequests = computed(() =>
  requests.value.filter(r => r.status === 'completed' || r.status === 'cancelled')
);

// Группировка активных по объектам
const groupedActiveRequests = computed(() => {
  const groups = new Map<number, {
    propertyId: number;
    propertyTitle: string;
    propertyAddress: string;
    requests: RequestWithDetails[];
  }>();

  for (const req of activeRequests.value) {
    const propId = req.property_info?.id || 0;
    if (!groups.has(propId)) {
      groups.set(propId, {
        propertyId: propId,
        propertyTitle: req.property_info?.title || '—',
        propertyAddress: req.property_info?.address || '',
        requests: [],
      });
    }
    groups.get(propId)!.requests.push(req);
  }

  return [...groups.values()];
});

const loadRequests = async () => {
  loading.value = true;
  try {
    requests.value = await requestsService.getOwnerRequests();
  } catch (err) {
    console.error('Ошибка загрузки заявок:', err);
  } finally {
    loading.value = false;
  }
};

const handleStatusChange = async (requestId: number, newStatus: string) => {
  await requestsService.updateRequestStatus(requestId, newStatus);
  loadRequests();
};

onMounted(loadRequests);
</script>

<style scoped>
.landlord-requests {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.75rem;
  color: #1f2937;
}

.refresh-btn {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  margin: 0 0 1rem 0;
}

.section-title--active {
  color: #dc2626;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.5rem;
  background: #e5e7eb;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.count-badge--active {
  background: #fecaca;
  color: #dc2626;
}

.count-badge--completed {
  background: #bbf7d0;
  color: #16a34a;
}

.property-group {
  margin-bottom: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
}

.group-title {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  color: #1f2937;
}

.group-address {
  color: #6b7280;
  font-size: 0.85rem;
  margin-left: 0.5rem;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.collapse-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 2rem;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}
</style>