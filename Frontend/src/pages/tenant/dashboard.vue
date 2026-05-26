<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Панель управления</h1>
        <p>Ваша информация по аренде</p>
      </div>
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка данных...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else class="dashboard-content">
      <!-- Active Contract -->
      <section v-if="activeContract" class="dashboard-section">
        <h2 class="section-title">Активный договор</h2>
        <Card class="contract-card">
          <template #content>
            <div class="contract-grid">
              <div class="contract-item">
                <span class="contract-label">Адрес недвижимости</span>
                <strong>{{ activeContract.property_id }}</strong>
              </div>
              <div class="contract-item">
                <span class="contract-label">Дата начала</span>
                <strong>{{ formatDate(activeContract.start_date) }}</strong>
              </div>
              <div class="contract-item">
                <span class="contract-label">Дата окончания</span>
                <strong>{{ formatDate(activeContract.end_date) }}</strong>
              </div>
              <div class="contract-item">
                <span class="contract-label">Статус</span>
                <Tag
                  :value="activeContract.status"
                  :severity="getStatusSeverity(activeContract.status)"
                />
              </div>
              <div class="contract-item">
                <span class="contract-label">Ежемесячный платёж</span>
                <strong class="amount">{{ formatAmount(activeContract.monthly_payment) }} ₽</strong>
              </div>
            </div>
          </template>
        </Card>
      </section>

      <!-- Upcoming Payments -->
      <section class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Предстоящие платежи</h2>
          <span v-if="unpaidPayments.length > 0" class="badge">
            {{ unpaidPayments.length }}
          </span>
        </div>

        <div v-if="unpaidPayments.length === 0" class="empty-state">
          <p>Все платежи оплачены</p>
        </div>

        <div v-else class="payments-list">
          <Card v-for="payment in upcomingPayments" :key="payment.id" class="payment-item">
            <template #content>
              <div class="payment-grid">
                <div class="payment-info">
                  <span class="payment-label">Сумма</span>
                  <strong class="amount">{{ formatAmount(payment.amount) }} ₽</strong>
                </div>
                <div class="payment-info">
                  <span class="payment-label">Срок</span>
                  <strong>{{ formatDate(payment.due_date) }}</strong>
                </div>
                <div class="payment-status">
                  <Tag
                    :value="payment.status"
                    :severity="getPaymentStatusSeverity(payment.status)"
                  />
                </div>
              </div>
            </template>
          </Card>
        </div>
      </section>

      <!-- Recent Requests -->
      <section class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Последние заявки</h2>
          <span v-if="activeRequests.length > 0" class="badge">
            {{ activeRequests.length }}
          </span>
        </div>

        <div v-if="activeRequests.length === 0" class="empty-state">
          <p>Активных заявок нет</p>
        </div>

        <div v-else class="requests-list">
          <Card v-for="request in recentRequests" :key="request.id" class="request-item">
            <template #content>
              <div class="request-grid">
                <div class="request-info">
                  <p class="request-message">{{ request.message }}</p>
                  <div class="request-meta">
                    <span class="request-date">{{ formatDate(request.created_at) }}</span>
                  </div>
                </div>
                <div class="request-status">
                  <Tag
                    :value="request.status"
                    :severity="getRequestStatusSeverity(request.status)"
                  />
                </div>
              </div>
            </template>
          </Card>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import Card from 'primevue/card';
import Tag from 'primevue/tag';
import { getContractsByTenant } from '../../services/mock/contracts';
import { getPaymentsByContract } from '../../services/mock/payments';
import { getRequestsByContract } from '../../services/mock/requests';
import { useAuthStore } from '../../stores/auth';
import type { Contract, Payment, Request } from '../../shared/types';

const authStore = useAuthStore();

const isLoading = ref(false);
const errorMessage = ref('');
const activeContract = ref<Contract | null>(null);
const payments = ref<Payment[]>([]);
const requests = ref<Request[]>([]);

const getTenantId = (): string => authStore.user?.id ?? 'user_3';

const unpaidPayments = computed(() =>
  payments.value.filter(p => p.status === 'unpaid' || p.status === 'overdue')
);

const upcomingPayments = computed(() =>
  unpaidPayments.value.sort((a, b) =>
    new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
  )
);

const activeRequests = computed(() =>
  requests.value.filter(r => r.status === 'new' || r.status === 'in_progress')
);

const recentRequests = computed(() =>
  activeRequests.value.sort((a, b) =>
    new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  ).slice(0, 3)
);

const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  } catch {
    return dateStr;
  }
};

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'decimal',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

const getStatusSeverity = (status: string): string => {
  const severityMap: Record<string, string> = {
    active: 'success',
    completed: 'info',
    cancelled: 'danger'
  };
  return severityMap[status] ?? 'secondary';
};

const getPaymentStatusSeverity = (status: string): string => {
  const severityMap: Record<string, string> = {
    paid: 'success',
    unpaid: 'warning',
    overdue: 'danger'
  };
  return severityMap[status] ?? 'secondary';
};

const getRequestStatusSeverity = (status: string): string => {
  const severityMap: Record<string, string> = {
    new: 'info',
    in_progress: 'warning',
    completed: 'success'
  };
  return severityMap[status] ?? 'secondary';
};

const loadDashboardData = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const tenantId = getTenantId();

    // Load contracts
    const contracts = await getContractsByTenant(tenantId);
    if (contracts.length === 0) {
      errorMessage.value = 'Активных договоров не найдено';
      return;
    }

    activeContract.value = contracts[0];

    // Load payments for the contract
    const contractPayments = await getPaymentsByContract(activeContract.value.id);
    payments.value = contractPayments;

    // Load requests for the contract
    const contractRequests = await getRequestsByContract(activeContract.value.id);
    requests.value = contractRequests;
  } catch {
    errorMessage.value = 'Не удалось загрузить данные. Попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(loadDashboardData);
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 1.5rem 2rem 2rem;
  overflow-x: hidden;
  overflow-y: auto;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
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
  min-height: 300px;
  padding: 2rem;
  color: #4b5563;
}

.state-loading {
  background: #f9fafb;
}

.state-error {
  border-color: #fecaca;
  background: #fef2f2;
  color: #991b1b;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.section-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.75rem;
  height: 1.75rem;
  background: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
}

/* Contract Card */
.contract-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.contract-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.contract-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contract-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.contract-item strong {
  font-size: 0.95rem;
  color: #111827;
  word-break: break-word;
}

.amount {
  font-size: 1rem;
  color: #1e40af;
  font-weight: 700;
}

/* Payments List */
.payments-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.payment-item {
  border: 1px solid #e5e7eb;
  border-radius: 0.6rem;
}

.payment-grid {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  align-items: center;
  gap: 1rem;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.payment-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.payment-info strong {
  font-size: 0.9rem;
  color: #111827;
}

.payment-status {
  display: flex;
  justify-content: flex-end;
}

/* Requests List */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.request-item {
  border: 1px solid #e5e7eb;
  border-radius: 0.6rem;
}

.request-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1rem;
  align-items: flex-start;
}

.request-info {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.request-message {
  margin: 0;
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.4;
  word-break: break-word;
}

.request-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.request-date {
  font-size: 0.75rem;
  color: #9ca3af;
}

.request-status {
  display: flex;
  justify-content: flex-end;
}

.empty-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 120px;
  border: 1px dashed #e5e7eb;
  border-radius: 0.75rem;
  background: #f9fafb;
  color: #9ca3af;
  text-align: center;
  padding: 1rem;
}

.empty-state p {
  margin: 0;
  font-size: 0.9rem;
}

/* PrimeVue Overrides */
:deep(.contract-card .p-card-body) {
  padding: 1rem 1.1rem;
}

:deep(.contract-card .p-card-content) {
  padding: 0;
}

:deep(.payment-item .p-card-body) {
  padding: 0.75rem 1rem;
}

:deep(.payment-item .p-card-content) {
  padding: 0;
}

:deep(.request-item .p-card-body) {
  padding: 0.75rem 1rem;
}

:deep(.request-item .p-card-content) {
  padding: 0;
}

:deep(.p-tag) {
  font-size: 0.7rem;
  padding: 0.35rem 0.65rem;
}

/* Responsive */
@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .contract-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .payment-grid {
    grid-template-columns: 1fr auto;
  }

  .request-grid {
    grid-template-columns: 1fr;
  }

  .request-status {
    justify-content: flex-start;
  }
}

@media (max-width: 640px) {
  .page-container {
    padding: 0.75rem;
  }

  .contract-grid {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 1.35rem;
  }
}
</style>
