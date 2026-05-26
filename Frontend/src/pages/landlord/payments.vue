<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Платежи</h1>
        <p>Платежи по договорам аренды</p>
      </div>

      <div class="filters">
        <label for="status-filter">Статус</label>
        <Select
          id="status-filter"
          v-model="selectedStatus"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          size="small"
        />
      </div>
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка платежей...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="filteredItems.length === 0" class="state state-empty">
      <h2>Платежей по выбранному фильтру нет</h2>
      <p>Попробуйте другой статус или добавьте новый договор.</p>
    </div>

    <div v-else class="payments-list">
      <Card
        v-for="item in filteredItems"
        :key="item.id"
        class="payment-card"
      >
        <template #content>
          <div class="payment-row">
            <div class="payment-main">
              <div class="line-title">
                <strong>{{ item.amount }}</strong>
                <Tag
                  :value="item.statusLabel"
                  :severity="item.statusSeverity"
                />
              </div>

              <div class="line-meta">
                <span>Срок оплаты: {{ item.dueDate }}</span>
                <span>{{ item.propertyTitle }}</span>
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import Card from 'primevue/card';
import Select from 'primevue/select';
import Tag from 'primevue/tag';
import type { PaymentStatus } from '../../shared/types';
import { getContractsByOwner } from '../../services/mock/contracts';
import { getPaymentsByContract } from '../../services/mock/payments';
import { getPropertyById } from '../../services/mock/properties';
import { useAuthStore } from '../../stores/auth';

type TagSeverity = 'secondary' | 'info' | 'success' | 'warn' | 'danger' | 'contrast';
type StatusFilter = 'all' | PaymentStatus;

interface PaymentItem {
  id: string;
  amount: string;
  dueDate: string;
  dueDateRaw: string;
  status: PaymentStatus;
  statusLabel: string;
  statusSeverity: TagSeverity;
  propertyTitle: string;
}

const authStore = useAuthStore();

const items = ref<PaymentItem[]>([]);
const isLoading = ref(false);
const errorMessage = ref('');
const selectedStatus = ref<StatusFilter>('all');

const statusOptions: Array<{ label: string; value: StatusFilter }> = [
  { label: 'Все', value: 'all' },
  { label: 'Оплачен', value: 'paid' },
  { label: 'Не оплачен', value: 'unpaid' },
  { label: 'Просрочен', value: 'overdue' },
];

const getOwnerId = (): string => authStore.user?.id ?? 'user_1';

const formatMoney = (value: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0,
  }).format(value);
};

const formatDate = (value: string): string => {
  return new Date(value).toLocaleDateString('ru-RU');
};

const statusMeta = (status: PaymentStatus): { label: string; severity: TagSeverity } => {
  if (status === 'paid') {
    return { label: 'Оплачен', severity: 'success' };
  }

  if (status === 'overdue') {
    return { label: 'Просрочен', severity: 'danger' };
  }

  return { label: 'Не оплачен', severity: 'warn' };
};

const filteredItems = computed(() => {
  if (selectedStatus.value === 'all') {
    return items.value;
  }

  return items.value.filter(item => item.status === selectedStatus.value);
});

const loadPayments = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const contracts = await getContractsByOwner(getOwnerId());

    const list = await Promise.all(
      contracts.map(async contract => {
        const [payments, property] = await Promise.all([
          getPaymentsByContract(contract.id),
          getPropertyById(contract.property_id),
        ]);

        return payments.map(payment => {
          const status = statusMeta(payment.status);
          return {
            id: payment.id,
            amount: formatMoney(payment.amount),
            dueDate: formatDate(payment.due_date),
            dueDateRaw: payment.due_date,
            status: payment.status,
            statusLabel: status.label,
            statusSeverity: status.severity,
            propertyTitle: property?.title ?? 'Неизвестный объект',
          } satisfies PaymentItem;
        });
      })
    );

    items.value = list
      .flat()
      .sort((a, b) => new Date(b.dueDateRaw).getTime() - new Date(a.dueDateRaw).getTime());
  } catch {
    errorMessage.value = 'Не удалось загрузить платежи. Попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(loadPayments);
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

.filters {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 180px;
}

.filters label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #4b5563;
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

.payments-list {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.payment-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.payment-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.payment-main {
  min-width: 0;
  flex: 1;
}

.line-title {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-bottom: 0.4rem;
}

.line-title strong {
  font-size: 1rem;
  color: #111827;
}

.line-meta {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  flex-wrap: wrap;
  color: #6b7280;
  font-size: 0.87rem;
}

:deep(.payment-card .p-card-body) {
  padding: 0.7rem 0.9rem;
}

:deep(.payment-card .p-card-content) {
  padding: 0;
}

@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filters {
    min-width: 0;
  }
}
</style>
