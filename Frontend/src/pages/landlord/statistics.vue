<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Статистика</h1>
        <p>Доходы и активность по недвижимости</p>
      </div>
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка статистики...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else class="stats-content">
      <!-- Key Metrics -->
      <section class="metrics-section">
        <div class="metrics-grid">
          <Card class="metric-card metric-income">
            <template #content>
              <div class="metric-wrapper">
                <span class="metric-label">Получено доходов</span>
                <strong class="metric-value">{{ formatAmount(stats.total_paid) }} ₽</strong>
              </div>
            </template>
          </Card>

          <Card class="metric-card metric-overdue">
            <template #content>
              <div class="metric-wrapper">
                <span class="metric-label">Просроченных платежей</span>
                <strong class="metric-value">{{ stats.overdue_count }}</strong>
              </div>
            </template>
          </Card>

          <Card class="metric-card metric-contracts">
            <template #content>
              <div class="metric-wrapper">
                <span class="metric-label">Активных договоров</span>
                <strong class="metric-value">{{ activeContractsCount }}</strong>
              </div>
            </template>
          </Card>

          <Card class="metric-card metric-pending">
            <template #content>
              <div class="metric-wrapper">
                <span class="metric-label">Ожидают платежа</span>
                <strong class="metric-value">{{ formatAmount(stats.total_unpaid) }} ₽</strong>
              </div>
            </template>
          </Card>
        </div>
      </section>

      <!-- Income Chart -->
      <section class="chart-section">
        <h2 class="section-title">Доход по объектам</h2>
        <Card class="chart-card">
          <template #content>
            <div v-if="chartData.labels.length > 0" class="chart-wrapper">
              <Chart
                :key="`chart-${chartData.labels.join('|')}`"
                type="bar"
                :data="chartData"
                :options="chartOptions"
                class="income-chart"
              />
            </div>
            <div v-else class="empty-chart">
              <p>Нет данных для отображения</p>
            </div>
          </template>
        </Card>
      </section>

      <!-- Payment Status Breakdown -->
      <section class="breakdown-section">
        <h2 class="section-title">Статус платежей</h2>
        <Card class="breakdown-card">
          <template #content>
            <div class="breakdown-grid">
              <div class="breakdown-item">
                <span class="breakdown-label">Оплачено</span>
                <strong class="breakdown-value paid">{{ formatAmount(stats.total_paid) }} ₽</strong>
              </div>
              <div class="breakdown-item">
                <span class="breakdown-label">Ожидают оплаты</span>
                <strong class="breakdown-value unpaid">{{ formatAmount(stats.total_unpaid) }} ₽</strong>
              </div>
              <div class="breakdown-item">
                <span class="breakdown-label">Просрочено</span>
                <strong class="breakdown-value overdue">{{ formatAmount(stats.total_overdue) }} ₽</strong>
              </div>
            </div>
          </template>
        </Card>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import Card from 'primevue/card';
import Chart from 'primevue/chart';
import { getContractsByOwner } from '../../services/mock/contracts';
import { getPaymentStats } from '../../services/mock/payments';
import { useAuthStore } from '../../stores/auth';
import type { Contract } from '../../shared/types';

const authStore = useAuthStore();

const isLoading = ref(false);
const errorMessage = ref('');
const stats = ref({
  total_paid: 0,
  total_unpaid: 0,
  total_overdue: 0,
  overdue_count: 0,
});
const contracts = ref<Contract[]>([]);

const getOwnerId = (): string => authStore.user?.id ?? 'user_1';

const activeContractsCount = computed(() =>
  contracts.value.filter(c => c.status === 'active').length
);

const chartData = computed(() => {
  const activeContracts = contracts.value.filter(c => c.status === 'active');
  return {
    labels: activeContracts.map(c => c.property_id),
    datasets: [
      {
        label: 'Ежемесячный доход (₽)',
        data: activeContracts.map(c => c.monthly_payment),
        backgroundColor: '#3b82f6',
        borderColor: '#1e40af',
        borderWidth: 1,
      },
    ],
  };
});

const chartOptions = {
  indexAxis: 'x' as const,
  maintainAspectRatio: true,
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: '#1f2937',
      titleColor: '#fff',
      bodyColor: '#fff',
      padding: 8,
      displayColors: false,
      callbacks: {
        label: (context: any) => {
          return `₽ ${(context.parsed.y || 0).toLocaleString('ru-RU')}`;
        },
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        color: '#6b7280',
        font: {
          size: 12,
        },
        callback: (value: any) => `₽ ${(value / 1000).toFixed(0)}k`,
      },
      grid: {
        color: '#e5e7eb',
        drawBorder: false,
      },
    },
    x: {
      ticks: {
        color: '#6b7280',
        font: {
          size: 12,
        },
      },
      grid: {
        display: false,
        drawBorder: false,
      },
    },
  },
};

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'decimal',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

const loadStatistics = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const ownerId = getOwnerId();

    // Load contracts
    const ownerContracts = await getContractsByOwner(ownerId);
    if (ownerContracts.length === 0) {
      errorMessage.value = 'Нет договоров для отображения статистики.';
      return;
    }

    contracts.value = ownerContracts;

    // Load payment statistics
    const paymentStats = await getPaymentStats(ownerId);
    stats.value = paymentStats;
  } catch {
    errorMessage.value = 'Не удалось загрузить статистику. Попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(loadStatistics);
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

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Metrics Section */
.metrics-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.9rem;
}

.metric-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background: white;
}

.metric-card.metric-income {
  border-left: 3px solid #10b981;
}

.metric-card.metric-overdue {
  border-left: 3px solid #ef4444;
}

.metric-card.metric-contracts {
  border-left: 3px solid #3b82f6;
}

.metric-card.metric-pending {
  border-left: 3px solid #f59e0b;
}

.metric-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.85rem 0;
}

.metric-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.metric-value {
  font-size: 1.35rem;
  font-weight: 700;
  color: #111827;
}

/* Chart Section */
.chart-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.section-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.chart-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.income-chart {
  height: 280px;
}

.chart-wrapper {
  width: 100%;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 280px;
  color: #9ca3af;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.empty-chart p {
  margin: 0;
  font-size: 0.9rem;
}

/* Breakdown Section */
.breakdown-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.breakdown-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.breakdown-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}

.breakdown-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding: 0.75rem 0;
  border-right: 1px solid #e5e7eb;
}

.breakdown-item:last-child {
  border-right: none;
}

.breakdown-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.breakdown-value {
  font-size: 1.25rem;
  font-weight: 700;
}

.breakdown-value.paid {
  color: #10b981;
}

.breakdown-value.unpaid {
  color: #f59e0b;
}

.breakdown-value.overdue {
  color: #ef4444;
}

/* PrimeVue Overrides */
:deep(.metric-card .p-card-body) {
  padding: 1rem 1.1rem;
}

:deep(.metric-card .p-card-content) {
  padding: 0;
}

:deep(.chart-card .p-card-body) {
  padding: 1.1rem;
}

:deep(.chart-card .p-card-content) {
  padding: 0;
}

:deep(.breakdown-card .p-card-body) {
  padding: 1rem 1.1rem;
}

:deep(.breakdown-card .p-card-content) {
  padding: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .income-chart {
    height: 240px;
  }

  .empty-chart {
    height: 240px;
  }
}

@media (max-width: 640px) {
  .page-container {
    padding: 0.75rem;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .breakdown-grid {
    grid-template-columns: 1fr;
  }

  .breakdown-item {
    border-right: none;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 0.85rem;
  }

  .breakdown-item:last-child {
    border-bottom: none;
  }

  h1 {
    font-size: 1.35rem;
  }

  .income-chart {
    height: 200px;
  }

  .empty-chart {
    height: 200px;
  }
}
</style>
