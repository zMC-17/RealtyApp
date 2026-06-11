<!-- pages/landlord/dashboard.vue -->
<template>
  <div class="content-page">
    <div class="content-inner">

      <header class="page-header">
        <div class="page-header-left">
          <p class="page-eyebrow">{{ currentDate }}</p>
          <h1 class="page-title">Дашборд</h1>
        </div>
        <button class="refresh-btn" @click="loadAllData" :disabled="loading">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" :class="{ spinning: loading }">
            <path d="M1.5 7A5.5 5.5 0 1 0 7 1.5a5.5 5.5 0 0 0-4.2 1.96" stroke="currentColor" stroke-width="1.4"
              stroke-linecap="round" />
            <path d="M1.5 1.5v3.5H5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
          Обновить
        </button>
      </header>

      <div v-if="loading" class="loading-state">
        <div class="loader-line"></div>
        <p class="loader-label">Загрузка данных…</p>
      </div>

      <template v-else>

        <!-- Метрики — стеклянные карточки -->
        <section class="metrics-section">
          <StatCard label="Объектов" :value="properties.length" />
          <StatCard label="Активных договоров" :value="activeContracts.length" />
          <StatCard label="Выручка за месяц" :value="formatCurrency(monthRevenue)" />
          <StatCard label="Ожидаемая выручка" :value="formatCurrency(expectedRevenue)" />
        </section>

        <!-- Алерты + График -->
        <section class="main-grid">

          <!-- Алерты -->
          <div class="glass-panel alerts-column">
            <h2 class="column-title">Статус</h2>

            <div v-if="!hasAlerts" class="all-good">
              <div class="all-good-dot"></div>
              <span>Всё в порядке</span>
            </div>

            <div v-else class="alerts-list">
              <div v-if="overduePayments.length > 0" class="alert-item alert-item--danger">
                <div class="alert-count">{{ overduePayments.length }}</div>
                <div class="alert-text">
                  <span class="alert-name">Просрочено</span>
                  <span class="alert-sub">{{ pluralize(overduePayments.length, 'платёж', 'платежа', 'платежей')
                    }}</span>
                </div>
                <div class="alert-badge alert-badge--danger">!</div>
              </div>

              <div v-if="waitingPayments.length > 0" class="alert-item alert-item--warning">
                <div class="alert-count">{{ waitingPayments.length }}</div>
                <div class="alert-text">
                  <span class="alert-name">На подтверждении</span>
                  <span class="alert-sub">{{ pluralize(waitingPayments.length, 'платёж', 'платежа', 'платежей')
                    }}</span>
                </div>
                <div class="alert-badge alert-badge--warning">~</div>
              </div>

              <div v-if="openRequests.length > 0" class="alert-item alert-item--info">
                <div class="alert-count">{{ openRequests.length }}</div>
                <div class="alert-text">
                  <span class="alert-name">Заявки</span>
                  <span class="alert-sub">{{ pluralize(openRequests.length, 'открытая', 'открытые', 'открытых')
                    }}</span>
                </div>
                <div class="alert-badge alert-badge--info">↗</div>
              </div>

              <div v-if="expiringContracts.length > 0" class="alert-item alert-item--neutral">
                <div class="alert-count">{{ expiringContracts.length }}</div>
                <div class="alert-text">
                  <span class="alert-name">Истекают</span>
                  <span class="alert-sub">{{ pluralize(expiringContracts.length, 'договор', 'договора', 'договоров') }}
                    в этом месяце</span>
                </div>
                <div class="alert-badge alert-badge--neutral">↻</div>
              </div>
            </div>

            <div class="occupancy-block">
              <div class="occupancy-header">
                <span class="occupancy-label">Заполняемость</span>
                <span class="occupancy-pct">{{ occupancyPct }}%</span>
              </div>
              <div class="occupancy-track">
                <div class="occupancy-fill" :style="{ width: occupancyPct + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- График -->
          <div class="glass-panel chart-column">
            <div class="chart-header">
              <h2 class="column-title">Выручка</h2>
              <span class="chart-period">6 месяцев</span>
            </div>
            <div class="chart-body">
              <RevenueChart :payments="allPayments" />
            </div>
          </div>

        </section>

      </template>
    </div>
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

const currentDate = computed(() =>
  new Date().toLocaleDateString('ru-RU', { weekday: 'long', day: 'numeric', month: 'long' })
);
const activeContracts = computed(() => contracts.value.filter(c => c.status === 'active'));
const occupancyPct = computed(() => {
  if (!properties.value.length) return 0;
  return Math.round((activeContracts.value.length / properties.value.length) * 100);
});
const monthRevenue = computed(() => {
  const now = new Date();
  return allPayments.value
    .filter(p => { if (p.status !== 'paid' || !p.paid_at) return false; const d = new Date(p.paid_at); return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear(); })
    .reduce((sum, p) => sum + parseFloat(p.amount), 0);
});
const expectedRevenue = computed(() => {
  const now = new Date(); const m = now.getMonth(), y = now.getFullYear();
  return allPayments.value
    .filter(p => { const due = new Date(p.due_date); const cur = due.getMonth() === m && due.getFullYear() === y; if (p.status === 'paid' && p.paid_at) { const pd = new Date(p.paid_at); return pd.getMonth() === m && pd.getFullYear() === y && cur; } return cur && ['pending', 'waiting_confirmation', 'overdue'].includes(p.status); })
    .reduce((sum, p) => sum + parseFloat(p.amount), 0);
});
const overduePayments = computed(() => allPayments.value.filter(p => p.status === 'overdue'));
const waitingPayments = computed(() => allPayments.value.filter(p => p.status === 'waiting_confirmation'));
const openRequests = computed(() => requests.value.filter(r => ['open', 'in_progress'].includes(r.status)));
const expiringContracts = computed(() => { const now = new Date(), soon = new Date(now.getTime() + 30 * 86400000); return activeContracts.value.filter(c => { const e = new Date(c.end_date); return e <= soon && e >= now; }); });
const hasAlerts = computed(() => overduePayments.value.length > 0 || waitingPayments.value.length > 0 || openRequests.value.length > 0 || expiringContracts.value.length > 0);

const loadAllData = async () => {
  loading.value = true;
  try {
    const [props, conts, pays, reqs] = await Promise.all([
      propertiesService.getMyProperties(), contractsService.getOwnerContracts(),
      paymentsService.getOwnerPayments(), requestsService.getOwnerRequests(),
    ]);
    properties.value = props; contracts.value = conts; allPayments.value = pays; requests.value = reqs;
  } catch (err) { console.error(err); }
  finally { loading.value = false; }
};

const formatCurrency = (v: number) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', minimumFractionDigits: 0 }).format(v);

const pluralize = (n: number, one: string, few: string, many: string) => {
  const m10 = n % 10, m100 = n % 100;
  if (m100 >= 11 && m100 <= 19) return many;
  if (m10 === 1) return one;
  if (m10 >= 2 && m10 <= 4) return few;
  return many;
};

onMounted(loadAllData);
</script>

<style scoped>
/* ---- Шапка ---- */
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

.refresh-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: rgba(255, 255, 255, 0.40);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.55);
  border-radius: var(--radius-md);
  color: var(--color-dark-60);
  font-family: var(--font-base);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.60);
  color: var(--color-dark);
}

.refresh-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ---- Лоадер ---- */
.loading-state {
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

/* ---- Метрики ---- */
.metrics-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

@media (max-width: 860px) {
  .metrics-section {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* ---- Сетка ---- */
.main-grid {
  display: grid;
  grid-template-columns: 256px 1fr;
  gap: var(--space-4);
  align-items: start;
}

@media (max-width: 860px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
}

/* ---- Стеклянная панель (общий класс для алертов и графика) ---- */
.glass-panel {
  background: rgba(255, 255, 255, 0.52);
  backdrop-filter: blur(20px) saturate(140%);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  border: 1px solid rgba(255, 255, 255, 0.65);
  border-radius: var(--radius-lg);
  box-shadow:
    0 2px 0 rgba(255, 255, 255, 0.70) inset,
    0 8px 32px rgba(28, 26, 23, 0.08);
}

/* ---- Алерты ---- */
.alerts-column {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.column-title {
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-dark-35);
}

.all-good {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-dark-60);
  font-weight: 500;
}

.all-good-dot {
  width: 8px;
  height: 8px;
  background: var(--color-emerald);
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 0 3px var(--color-emerald-20);
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.alert-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  /* Полупрозрачный фон алерта поверх стеклянной панели */
  background: rgba(255, 255, 255, 0.50);
  border: 1px solid transparent;
}

.alert-item--danger {
  border-color: rgba(185, 64, 64, 0.18);
}

.alert-item--warning {
  border-color: rgba(184, 115, 51, 0.18);
}

.alert-item--info {
  border-color: rgba(58, 110, 143, 0.18);
}

.alert-item--neutral {
  border-color: rgba(122, 107, 138, 0.18);
}

.alert-count {
  font-size: var(--text-xl);
  font-weight: 800;
  color: var(--color-dark);
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
  min-width: 24px;
  line-height: 1;
}

.alert-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.alert-name {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-dark);
}

.alert-sub {
  font-size: var(--text-xs);
  color: var(--color-dark-35);
}

.alert-badge {
  width: 20px;
  height: 20px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.alert-badge--danger {
  background: var(--color-danger-bg);
  color: var(--color-danger);
}

.alert-badge--warning {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.alert-badge--info {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.alert-badge--neutral {
  background: var(--color-neutral-bg);
  color: var(--color-neutral);
}

/* ---- Заполняемость ---- */
.occupancy-block {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding-top: var(--space-4);
  border-top: 1px solid rgba(28, 26, 23, 0.08);
}

.occupancy-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.occupancy-label {
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-dark-35);
}

.occupancy-pct {
  font-size: var(--text-md);
  font-weight: 800;
  color: var(--color-emerald);
  font-variant-numeric: tabular-nums;
}

.occupancy-track {
  height: 3px;
  background: rgba(28, 26, 23, 0.10);
  border-radius: 2px;
  overflow: hidden;
}

.occupancy-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-emerald), var(--color-olive));
  border-radius: 2px;
  transition: width 800ms ease;
}

/* ---- График ---- */
.chart-column {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chart-period {
  font-size: var(--text-xs);
  color: var(--color-dark-35);
  font-weight: 500;
}

.chart-body {
  height: 220px;
}
</style>