<!-- pages/tenant/requests.vue -->
<template>
  <div class="content-page">
    <div class="content-inner">

      <header class="page-header">
        <div>
          <p class="page-eyebrow">Обслуживание</p>
          <h1 class="page-title">Заявки</h1>
        </div>
        <button v-if="activeContractId" class="btn-dark" @click="showCreateModal = true">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          Новая заявка
        </button>
      </header>

      <!-- Лоадер -->
      <div v-if="loading" class="loader-wrap">
        <div class="loader-line"></div>
        <p class="loader-label">Загрузка заявок…</p>
      </div>

      <!-- Пусто -->
      <div v-else-if="requests.length === 0" class="empty-state">
        <div class="empty-icon-box">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M17 3H3a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h4l3 3 3-3h4a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1Z"
              stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" />
            <path d="M6 8h8M6 12h5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
          </svg>
        </div>
        <p class="empty-title">Заявок пока нет</p>
        <p class="empty-text">
          {{ activeContractId ? 'Создайте заявку, если требуется обслуживание объекта' : 'У вас нет активного договора'
          }}
        </p>
        <button v-if="activeContractId" class="btn-dark" style="margin-top: var(--space-2)"
          @click="showCreateModal = true">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          Создать первую заявку
        </button>
      </div>

      <template v-else>

        <!-- Активные -->
        <section v-if="activeRequests.length > 0" class="section">
          <div class="section-head">
            <h2 class="section-title">Активные</h2>
            <span class="count-pill count-pill--danger">{{ activeRequests.length }}</span>
          </div>
          <div class="requests-list">
            <RequestCard v-for="req in activeRequests" :key="req.id" :request="req" :show-actions="false" />
          </div>
        </section>

        <!-- Завершённые — схлопываются -->
        <section v-if="completedRequests.length > 0" class="section">
          <button class="collapse-btn" @click="showCompleted = !showCompleted">
            <span class="collapse-icon" :class="{ rotated: showCompleted }">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </span>
            Завершённые и отменённые
            <span class="count-pill count-pill--success">{{ completedRequests.length }}</span>
          </button>
          <div v-if="showCompleted" class="requests-list requests-list--collapsed">
            <RequestCard v-for="req in completedRequests" :key="req.id" :request="req" :show-actions="false" />
          </div>
        </section>

      </template>
    </div>
  </div>

  <CreateRequestModal v-if="showCreateModal" :visible="showCreateModal" :contract-id="activeContractId!"
    @close="showCreateModal = false" @created="onRequestCreated" />
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
const activeRequests = computed(() => requests.value.filter(r => ['open', 'in_progress'].includes(r.status)));
const completedRequests = computed(() => requests.value.filter(r => ['completed', 'cancelled'].includes(r.status)));

async function loadRequests() {
  loading.value = true;
  try { requests.value = await requestsService.getTenantRequests(); }
  catch (err) { console.error(err); }
  finally { loading.value = false; }
}

function onRequestCreated() {
  showCreateModal.value = false;
  loadRequests();
}

onMounted(loadRequests);
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: var(--space-8);
}

.page-eyebrow {
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-dark-35);
  margin-bottom: var(--space-1);
}

.page-title {
  font-size: var(--text-3xl);
  font-weight: 800;
  color: var(--color-dark);
  letter-spacing: -0.03em;
  line-height: 1;
}

.btn-dark {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
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
  box-shadow: 0 4px 16px rgba(28, 26, 23, 0.20);
  transform: translateY(-1px);
}

.btn-dark:active {
  transform: translateY(0);
}

/* ---- Лоадер ---- */
.loader-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-16);
}

.loader-line {
  width: 160px;
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

/* ---- Пустое ---- */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-16) var(--space-8);
  text-align: center;
}

.empty-icon-box {
  width: 52px;
  height: 52px;
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
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-dark);
  letter-spacing: -0.02em;
}

.empty-text {
  font-size: var(--text-sm);
  color: var(--color-dark-35);
  max-width: 300px;
}

/* ---- Секции ---- */
.section {
  margin-bottom: var(--space-10);
}

.section-head {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-dark-35);
}

.count-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 20px;
  padding: 0 var(--space-2);
  background: rgba(28, 26, 23, 0.08);
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--color-dark-60);
}

.count-pill--danger {
  background: var(--color-danger-bg);
  color: var(--color-danger);
}

.count-pill--success {
  background: var(--color-success-bg);
  color: var(--color-success);
}

/* ---- Списки ---- */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.requests-list--collapsed {
  margin-top: var(--space-3);
}

/* ---- Схлопывание ---- */
.collapse-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: rgba(255, 255, 255, 0.42);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.60);
  border-radius: var(--radius-md);
  font-family: var(--font-base);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-dark-60);
  cursor: pointer;
  transition: all var(--transition);
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.60);
  color: var(--color-dark);
}

.collapse-icon {
  display: flex;
  align-items: center;
  transition: transform var(--transition);
  color: var(--color-dark-35);
}

.collapse-icon.rotated {
  transform: rotate(180deg);
}
</style>