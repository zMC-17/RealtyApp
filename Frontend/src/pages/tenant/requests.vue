<!-- pages/tenant/requests.vue -->
<template>
  <div class="tenant-requests">
    <div class="page-header">
      <h1>Заявки</h1>
      <button v-if="activeContractId" class="btn-create" @click="showCreateModal = true">
        + Создать заявку
      </button>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка заявок...</p>
    </div>

    <div v-else-if="requests.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <h2>Заявок пока нет</h2>
      <p v-if="activeContractId">Создайте заявку, если требуется обслуживание</p>
      <p v-else>У вас нет активного договора</p>
    </div>

    <template v-else>
      <!-- Активные заявки -->
      <section v-if="activeRequests.length > 0" class="section">
        <h2 class="section-title section-title--active">
          <span>📋</span> Активные
          <span class="count-badge count-badge--active">{{ activeRequests.length }}</span>
        </h2>
        <div class="requests-list">
          <RequestCard v-for="req in activeRequests" :key="req.id" :request="req" :show-actions="false" />
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
          <RequestCard v-for="req in completedRequests" :key="req.id" :request="req" :show-actions="false" />
        </div>
      </section>
    </template>

    <CreateRequestModal v-if="showCreateModal" :visible="showCreateModal" :contract-id="activeContractId!"
      @close="showCreateModal = false" @created="onRequestCreated" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { requestsService } from '../../services/requests';
import { useTenantStore } from '../../stores/tenant';
import type { RequestWithDetails } from '../../types/request';
import RequestCard from '../../components/requests/RequestCard.vue';
import CreateRequestModal from '../../components/requests/CreateRequestModal.vue';

const tenantStore = useTenantStore();
const requests = ref<RequestWithDetails[]>([]);
const loading = ref(true);
const showCompleted = ref(false);
const showCreateModal = ref(false);

const activeContractId = computed(() => tenantStore.activeContract?.id || null);

const activeRequests = computed(() =>
  requests.value.filter(r => r.status === 'open' || r.status === 'in_progress')
);

const completedRequests = computed(() =>
  requests.value.filter(r => r.status === 'completed' || r.status === 'cancelled')
);

const loadRequests = async () => {
  loading.value = true;
  try {
    requests.value = await requestsService.getTenantRequests();
  } catch (err) {
    console.error('Ошибка загрузки заявок:', err);
  } finally {
    loading.value = false;
  }
};

const onRequestCreated = () => {
  showCreateModal.value = false;
  loadRequests();
};

onMounted(loadRequests);
</script>

<style scoped>
.tenant-requests {
  padding: 2rem;
  max-width: 800px;
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

.btn-create {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-create:hover {
  transform: translateY(-1px);
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

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
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