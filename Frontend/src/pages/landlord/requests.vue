<!-- pages/landlord/requests.vue -->
<template>
  <div class="content-page">
    <div class="content-inner">

      <header class="page-header">
        <div>
          <p class="page-eyebrow">Обслуживание</p>
          <h1 class="page-title">Заявки</h1>
        </div>
        <button class="btn-ghost" @click="loadRequests" :disabled="loading">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"
            :style="{ animation: loading ? 'spin 1s linear infinite' : 'none' }">
            <path d="M1.5 7A5.5 5.5 0 1 0 7 1.5a5.5 5.5 0 0 0-4.2 1.96" stroke="currentColor" stroke-width="1.4"
              stroke-linecap="round" />
            <path d="M1.5 1.5v3.5H5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
          Обновить
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
        <p class="empty-text">Когда арендаторы создадут заявки, они появятся здесь</p>
      </div>

      <template v-else>

        <!-- Активные — сгруппированы по объектам -->
        <section v-if="activeRequests.length > 0" class="section">
          <div class="section-head">
            <h2 class="section-title">Активные</h2>
            <span class="count-pill count-pill--danger">{{ activeRequests.length }}</span>
          </div>

          <!-- Группа по объекту -->
          <div v-for="group in groupedActiveRequests" :key="group.propertyId" class="property-group">
            <div class="group-header">
              <svg width="12" height="13" viewBox="0 0 12 13" fill="none">
                <path d="M1 6L6 1.5 11 6v5.5a.5.5 0 0 1-.5.5H8V9H4v3H1.5a.5.5 0 0 1-.5-.5V6Z" stroke="currentColor"
                  stroke-width="1.2" stroke-linejoin="round" />
              </svg>
              <span class="group-title">{{ group.propertyTitle }}</span>
              <span v-if="group.propertyAddress" class="group-address">{{ group.propertyAddress }}</span>
              <span class="group-count">{{ group.requests.length }}</span>
            </div>

            <div class="requests-list">
              <RequestCard v-for="req in group.requests" :key="req.id" :request="req" :show-actions="true"
                @status-change="handleStatusChange" />
            </div>
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
            <span class="count-pill">{{ completedRequests.length }}</span>
          </button>

          <div v-if="showCompleted" class="requests-list requests-list--collapsed">
            <RequestCard v-for="req in completedRequests" :key="req.id" :request="req" :show-actions="false" />
          </div>
        </section>

      </template>
    </div>
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

const activeRequests = computed(() => requests.value.filter(r => ['open', 'in_progress'].includes(r.status)));
const completedRequests = computed(() => requests.value.filter(r => ['completed', 'cancelled'].includes(r.status)));

const groupedActiveRequests = computed(() => {
  const groups = new Map<number, {
    propertyId: number; propertyTitle: string; propertyAddress: string;
    requests: RequestWithDetails[];
  }>();

  for (const req of activeRequests.value) {
    const id = req.property_info?.id ?? 0;
    if (!groups.has(id)) {
      groups.set(id, {
        propertyId: id,
        propertyTitle: req.property_info?.title || '—',
        propertyAddress: req.property_info?.address || '',
        requests: [],
      });
    }
    groups.get(id)!.requests.push(req);
  }

  return [...groups.values()];
});

async function loadRequests() {
  loading.value = true;
  try { requests.value = await requestsService.getOwnerRequests(); }
  catch (err) { console.error(err); }
  finally { loading.value = false; }
}

async function handleStatusChange(requestId: number, newStatus: string) {
  await requestsService.updateRequestStatus(requestId, newStatus);
  loadRequests();
}

onMounted(loadRequests);
</script>

<style scoped>
/* ---- Шапка страницы ---- */
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

.btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: rgba(255, 255, 255, 0.50);
  border: 1px solid rgba(255, 255, 255, 0.65);
  border-radius: var(--radius-md);
  color: var(--color-dark-60);
  font-family: var(--font-base);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);
  backdrop-filter: blur(8px);
}

.btn-ghost:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.72);
  color: var(--color-dark);
}

.btn-ghost:disabled {
  opacity: 0.4;
  cursor: not-allowed;
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

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loader-label {
  font-size: var(--text-sm);
  color: var(--color-dark-35);
}

/* ---- Пустое состояние ---- */
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
  margin-bottom: var(--space-5);
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

/* ---- Группа по объекту ---- */
.property-group {
  margin-bottom: var(--space-5);
}

.group-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4) var(--space-3) var(--space-4);
  margin-bottom: var(--space-2);
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.55);
  border-radius: var(--radius-md);
  color: var(--color-dark-35);
}

.group-title {
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--color-dark);
  letter-spacing: -0.01em;
}

.group-address {
  font-size: var(--text-xs);
  color: var(--color-dark-35);
  flex: 1;
  /* сдвигает каунт вправо */
}

.group-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 18px;
  padding: 0 var(--space-2);
  background: rgba(28, 26, 23, 0.07);
  border-radius: 9px;
  font-size: 10px;
  font-weight: 700;
  color: var(--color-dark-60);
  margin-left: auto;
}

/* ---- Список заявок ---- */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.requests-list--collapsed {
  margin-top: var(--space-3);
}

/* ---- Кнопка схлопывания ---- */
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