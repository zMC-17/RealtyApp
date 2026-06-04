<!-- pages/landlord/dashboard.vue -->
<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>Дашборд</h1>
      <button class="refresh-btn" @click="loadAllData" :disabled="loading">
        🔄 Обновить
      </button>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка данных...</p>
    </div>

    <template v-else>
      <!-- Карточки показателей -->
      <div class="stats-grid">
        <StatCard icon="📦" label="Всего объектов" :value="properties.length" color="#667eea" />
        <StatCard icon="📋" label="Активных договоров" :value="activeContracts.length" color="#10b981" />
        <StatCard icon="💰" label="Выручка за месяц" :value="formatCurrency(monthRevenue)" color="#f59e0b" />
        <StatCard icon="📈" label="Ожидаемая выручка" :value="formatCurrency(expectedRevenue)" color="#3b82f6" />
      </div>

      <!-- Блок проблем (только если есть) -->
      <section v-if="hasAlerts" class="alerts-section">
        <h2 class="section-title">
          <span>⚠️</span> Требуют внимания
        </h2>
        <div class="alerts-grid">
          <div v-if="overduePayments.length > 0" class="alert-card alert-card--danger">
            <span class="alert-icon">🔴</span>
            <div>
              <strong>{{ overduePayments.length }}</strong>
              <span>{{ pluralize(overduePayments.length, 'просроченный платёж', 'просроченных платежа', 'просроченных платежей') }}</span>
            </div>
          </div>
          <div v-if="waitingPayments.length > 0" class="alert-card alert-card--warning">
            <span class="alert-icon">🔍</span>
            <div>
              <strong>{{ waitingPayments.length }}</strong>
              <span>{{ pluralize(waitingPayments.length, 'платёж', 'платежа', 'платежей') }} на подтверждении</span>
            </div>
          </div>
          <div v-if="openRequests.length > 0" class="alert-card alert-card--info">
            <span class="alert-icon">📝</span>
            <div>
              <strong>{{ openRequests.length }}</strong>
              <span>{{ pluralize(openRequests.length, 'открытая заявка', 'открытые заявки', 'открытых заявок') }}</span>
            </div>
          </div>
          <div v-if="expiringContracts.length > 0" class="alert-card alert-card--neutral">
            <span class="alert-icon">⏳</span>
            <div>
              <strong>{{ expiringContracts.length }}</strong>
              <span>{{ pluralize(expiringContracts.length, 'договор', 'договора', 'договоров') }} заканчивается в этом
                месяце</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Нет проблем -->
      <div v-else class="all-good">
        <span class="all-good-icon">✅</span>
        <p>Всё в порядке, проблем нет</p>
      </div>

      <!-- График выручки -->
      <section class="chart-section">
        <h2 class="section-title">
          <span>📈</span> Выручка по месяцам
        </h2>
        <div class="chart-container">
          <RevenueChart :payments="allPayments" />
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { propertiesService } from '../../services/properties';
import { contractsService } from '../../services/contracts';
import { paymentsService } from '../../services/payments';
import { requestsService } from '../../services/requests';
import type { PropertyResponse } from '../../types/property';
import type { ContractResponse } from '../../types/contract';
import type { PaymentResponse } from '../../types/payment';
import type { RequestWithDetails } from '../../types/request';
import StatCard from '../../components/dashboard/StatCard.vue';
import RevenueChart from '../../components/dashboard/RevenueChart.vue';

const loading = ref(true);

const properties = ref<PropertyResponse[]>([]);
const contracts = ref<ContractResponse[]>([]);
const allPayments = ref<PaymentResponse[]>([]);
const requests = ref<RequestWithDetails[]>([]);

// Активные договоры
const activeContracts = computed(() =>
  contracts.value.filter(c => c.status === 'active')
);

// Выручка за текущий месяц
const monthRevenue = computed(() => {
  const now = new Date();
  const currentMonth = now.getMonth();
  const currentYear = now.getFullYear();

  return allPayments.value
    .filter(p => {
      if (p.status !== 'paid' || !p.paid_at) return false;
      const paidDate = new Date(p.paid_at);
      return paidDate.getMonth() === currentMonth && paidDate.getFullYear() === currentYear;
    })
    .reduce((sum, p) => sum + parseFloat(p.amount), 0);
});

// Ожидаемая выручка (pending + waiting + overdue платежи)
// Замените expectedRevenue:

const expectedRevenue = computed(() => {
  const now = new Date();
  const currentMonth = now.getMonth();
  const currentYear = now.getFullYear();

  return allPayments.value
    .filter(p => {
      // Исключаем cancelled и другие нерелевантные статусы
      if (p.status === 'cancelled') return false;

      // Платёж относится к текущему месяцу?
      const dueDate = new Date(p.due_date);
      const isCurrentMonth = dueDate.getMonth() === currentMonth && dueDate.getFullYear() === currentYear;

      // Уже оплачен в этом месяце
      if (p.status === 'paid' && p.paid_at) {
        const paidDate = new Date(p.paid_at);
        // Оплата проведена в текущем месяце И платёж запланирован на текущий месяц
        return paidDate.getMonth() === currentMonth && paidDate.getFullYear() === currentYear && isCurrentMonth;
      }

      // Ещё не оплачен, но запланирован на текущий месяц
      if (p.status === 'pending' || p.status === 'waiting_confirmation' || p.status === 'overdue') {
        return isCurrentMonth;
      }

      return false;
    })
    .reduce((sum, p) => sum + parseFloat(p.amount), 0);
});

// Просроченные платежи
const overduePayments = computed(() =>
  allPayments.value.filter(p => p.status === 'overdue')
);

// Платежи на подтверждении
const waitingPayments = computed(() =>
  allPayments.value.filter(p => p.status === 'waiting_confirmation')
);

// Открытые заявки
const openRequests = computed(() =>
  requests.value.filter(r => r.status === 'open' || r.status === 'in_progress')
);

// Заканчивающиеся договоры (в течение 30 дней)
const expiringContracts = computed(() => {
  const now = new Date();
  const thirtyDaysLater = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);

  return activeContracts.value.filter(c => {
    const endDate = new Date(c.end_date);
    return endDate <= thirtyDaysLater && endDate >= now;
  });
});

// Есть ли какие-то проблемы
const hasAlerts = computed(() =>
  overduePayments.value.length > 0 ||
  waitingPayments.value.length > 0 ||
  openRequests.value.length > 0 ||
  expiringContracts.value.length > 0
);

const loadAllData = async () => {
  loading.value = true;
  try {
    const [props, conts, pays, reqs] = await Promise.all([
      propertiesService.getMyProperties(),
      contractsService.getOwnerContracts(),
      paymentsService.getOwnerPayments(),
      requestsService.getOwnerRequests(),
    ]);
    properties.value = props;
    contracts.value = conts;
    allPayments.value = pays;
    requests.value = reqs;
  } catch (err) {
    console.error('Ошибка загрузки данных дашборда:', err);
  } finally {
    loading.value = false;
  }
};

const formatCurrency = (value: number) =>
  new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
  }).format(value);

const pluralize = (count: number, one: string, few: string, many: string) => {
  const mod10 = count % 10;
  const mod100 = count % 100;
  if (mod100 >= 11 && mod100 <= 19) return many;
  if (mod10 === 1) return one;
  if (mod10 >= 2 && mod10 <= 4) return few;
  return many;
};

onMounted(loadAllData);
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
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
  font-size: 0.875rem;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.alerts-section {
  margin-bottom: 2rem;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 12px;
  padding: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  margin: 0 0 1rem 0;
  color: #1f2937;
}

.alerts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
}

.alert-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: white;
  border-radius: 10px;
  border-left: 4px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.alert-card--danger {
  border-left-color: #ef4444;
}

.alert-card--warning {
  border-left-color: #f59e0b;
}

.alert-card--info {
  border-left-color: #3b82f6;
}

.alert-card--neutral {
  border-left-color: #8b5cf6;
}

.alert-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.alert-card strong {
  display: block;
  font-size: 1.25rem;
  color: #1f2937;
}

.alert-card span {
  font-size: 0.8rem;
  color: #6b7280;
}

.all-good {
  text-align: center;
  padding: 1.5rem;
  background: #f0fdf4;
  border: 1px solid #86efac;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.all-good-icon {
  font-size: 2rem;
}

.all-good p {
  color: #166534;
  margin: 0.5rem 0 0 0;
}

.chart-section {
  margin-bottom: 2rem;
}

.chart-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  max-height: 350px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 2rem;
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
</style>