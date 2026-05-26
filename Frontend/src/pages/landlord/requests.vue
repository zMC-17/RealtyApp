<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Заявки от арендаторов</h1>
        <p>Управление обращениями на обслуживание и ремонт</p>
      </div>
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка заявок...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="requestItems.length === 0" class="state state-empty">
      <h2>Заявок пока нет</h2>
      <p>Новые обращения появятся здесь автоматически.</p>
    </div>

    <div v-else class="requests-list">
      <Card
        v-for="item in requestItems"
        :key="item.id"
        class="request-card"
      >
        <template #content>
          <div class="request-row">
            <div class="request-main">
              <p class="message">{{ item.message }}</p>

              <div class="meta-line">
                <span>Договор: {{ item.contractReference }}</span>
                <span>Создано: {{ item.createdAt }}</span>
                <Tag :value="item.statusLabel" :severity="item.statusSeverity" />
              </div>
            </div>

            <div class="status-control">
              <label :for="`status-${item.id}`">Статус</label>
              <Select
                :id="`status-${item.id}`"
                :modelValue="item.status"
                :options="statusOptions"
                optionLabel="label"
                optionValue="value"
                size="small"
                :disabled="isUpdatingId === item.id"
                @update:modelValue="value => handleStatusChange(item.id, value)"
              />
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Card from 'primevue/card';
import Select from 'primevue/select';
import Tag from 'primevue/tag';
import type { RequestStatus } from '../../shared/types';
import { getContractsByOwner } from '../../services/mock/contracts';
import { getRequestsByContract, updateRequestStatus } from '../../services/mock/requests';
import { useAuthStore } from '../../stores/auth';

type TagSeverity = 'secondary' | 'info' | 'success' | 'warn' | 'danger' | 'contrast';

interface RequestItem {
  id: string;
  message: string;
  contractReference: string;
  createdAt: string;
  createdAtRaw: string;
  status: RequestStatus;
  statusLabel: string;
  statusSeverity: TagSeverity;
}

const authStore = useAuthStore();

const requestItems = ref<RequestItem[]>([]);
const isLoading = ref(false);
const errorMessage = ref('');
const isUpdatingId = ref<string | null>(null);

const statusOptions: Array<{ label: string; value: RequestStatus }> = [
  { label: 'Новая', value: 'new' },
  { label: 'В работе', value: 'in_progress' },
  { label: 'Выполнена', value: 'completed' },
];

const getOwnerId = (): string => authStore.user?.id ?? 'user_1';

const formatDate = (value: string): string => new Date(value).toLocaleDateString('ru-RU');

const statusMeta = (status: RequestStatus): { label: string; severity: TagSeverity } => {
  if (status === 'new') {
    return { label: 'Новая', severity: 'warn' };
  }

  if (status === 'in_progress') {
    return { label: 'В работе', severity: 'info' };
  }

  return { label: 'Выполнена', severity: 'success' };
};

const loadRequests = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const contracts = await getContractsByOwner(getOwnerId());

    const nestedRequests = await Promise.all(
      contracts.map(async contract => {
        const requests = await getRequestsByContract(contract.id);

        return requests.map(request => {
          const status = statusMeta(request.status);
          return {
            id: request.id,
            message: request.message,
            contractReference: contract.id,
            createdAt: formatDate(request.created_at),
            createdAtRaw: request.created_at,
            status: request.status,
            statusLabel: status.label,
            statusSeverity: status.severity,
          } satisfies RequestItem;
        });
      })
    );

    requestItems.value = nestedRequests
      .flat()
      .sort((a, b) => new Date(b.createdAtRaw).getTime() - new Date(a.createdAtRaw).getTime());
  } catch {
    errorMessage.value = 'Не удалось загрузить заявки. Попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

const handleStatusChange = async (requestId: string, nextStatus: RequestStatus) => {
  const current = requestItems.value.find(item => item.id === requestId);
  if (!current || current.status === nextStatus) {
    return;
  }

  isUpdatingId.value = requestId;
  errorMessage.value = '';

  try {
    const updated = await updateRequestStatus(requestId, nextStatus);
    if (!updated) {
      errorMessage.value = 'Не удалось обновить статус заявки.';
      return;
    }

    const status = statusMeta(updated.status);
    requestItems.value = requestItems.value.map(item =>
      item.id === requestId
        ? {
            ...item,
            status: updated.status,
            statusLabel: status.label,
            statusSeverity: status.severity,
          }
        : item
    );
  } catch {
    errorMessage.value = 'Ошибка обновления статуса. Попробуйте снова.';
  } finally {
    isUpdatingId.value = null;
  }
};

onMounted(loadRequests);
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 1.5rem 2rem 2rem;
  overflow-x: hidden;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  font-size: 1.625rem;
  font-weight: 700;
  color: #1f2937;
}

p {
  color: #6b7280;
  margin: 0.35rem 0 0;
  font-size: 0.95rem;
}

.state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  border: 1px dashed #d1d5db;
  border-radius: 0.75rem;
  min-height: 220px;
  padding: 1.25rem;
  color: #4b5563;
}

.state-empty h2 {
  margin: 0;
  font-size: 1.125rem;
  color: #111827;
}

.state-empty p {
  margin: 0.45rem 0 0;
}

.state-error {
  border-color: #fecaca;
  background: #fef2f2;
  color: #991b1b;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.request-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.request-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.9rem;
}

.request-main {
  min-width: 0;
  flex: 1;
}

.message {
  margin: 0 0 0.55rem;
  color: #111827;
  font-size: 0.95rem;
  line-height: 1.45;
}

.meta-line {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  flex-wrap: wrap;
  color: #6b7280;
  font-size: 0.84rem;
}

.status-control {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 170px;
}

.status-control label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #4b5563;
}

:deep(.request-card .p-card-body) {
  padding: 0.72rem 0.9rem;
}

:deep(.request-card .p-card-content) {
  padding: 0;
}

@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .request-row {
    flex-direction: column;
  }

  .status-control {
    min-width: 0;
    width: 100%;
  }
}
</style>
