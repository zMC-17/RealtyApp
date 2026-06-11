<!-- pages/tenant/payments.vue -->
<template>
  <div class="content-page">
    <div class="content-inner">

      <header class="page-header">
        <div>
          <p class="page-eyebrow">Финансы</p>
          <h1 class="page-title">Платежи</h1>
        </div>
        <button class="btn-ghost" @click="loadPayments" :disabled="loading">
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
        <p class="loader-label">Загрузка платежей…</p>
      </div>

      <!-- Пусто -->
      <div v-else-if="payments.length === 0" class="empty-state">
        <div class="empty-icon-box">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <rect x="2" y="5" width="16" height="12" rx="2" stroke="currentColor" stroke-width="1.4" />
            <path d="M2 9h16" stroke="currentColor" stroke-width="1.4" />
            <circle cx="5.5" cy="13" r="1" fill="currentColor" />
          </svg>
        </div>
        <p class="empty-title">Платежей пока нет</p>
        <p class="empty-text">Платежи появятся после активации договора</p>
      </div>

      <template v-else>

        <!-- Требуют оплаты -->
        <section v-if="urgentPayments.length > 0" class="payments-section payments-section--urgent">
          <div class="section-head">
            <h2 class="section-title">Требуют оплаты</h2>
            <span class="count-pill count-pill--danger">{{ urgentPayments.length }}</span>
          </div>
          <div class="list-header">
            <div class="lh-date">Дата</div>
            <div class="lh-status">Статус</div>
            <div class="lh-amount">Сумма</div>
            <div class="lh-action"></div>
          </div>
          <div class="payments-list">
            <TenantPaymentCard v-for="payment in urgentPayments" :key="payment.id" :payment="payment"
              @send-proof="openProofModal" />
          </div>
        </section>

        <!-- На подтверждении -->
        <section v-if="waitingPayments.length > 0" class="payments-section">
          <div class="section-head">
            <h2 class="section-title">На подтверждении</h2>
            <span class="count-pill count-pill--info">{{ waitingPayments.length }}</span>
          </div>
          <div class="list-header">
            <div class="lh-date">Дата</div>
            <div class="lh-status">Статус</div>
            <div class="lh-amount">Сумма</div>
            <div class="lh-action"></div>
          </div>
          <div class="payments-list">
            <TenantPaymentCard v-for="payment in waitingPayments" :key="payment.id" :payment="payment" />
          </div>
        </section>

        <!-- Оплаченные — схлопываются -->
        <section v-if="paidPayments.length > 0" class="payments-section">
          <button class="collapse-btn" @click="showPaid = !showPaid">
            <span class="collapse-icon" :class="{ rotated: showPaid }">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </span>
            Оплаченные
            <span class="count-pill count-pill--success">{{ paidPayments.length }}</span>
          </button>
          <div v-if="showPaid" class="payments-list payments-list--collapsed">
            <TenantPaymentCard v-for="payment in paidPayments" :key="payment.id" :payment="payment" />
          </div>
        </section>

      </template>
    </div>
  </div>

  <RequestConfirmationModal v-if="showProofModal && selectedPayment" :visible="showProofModal"
    :payment="selectedPayment" @close="showProofModal = false" @sent="onProofSent" />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { paymentsService } from '../../services/payments';
import type { PaymentResponse } from '../../types/payment';
import TenantPaymentCard from '../../components/tenant/TenantPaymentCard.vue';
import RequestConfirmationModal from '../../components/payments/RequestConfirmationModal.vue';

const payments = ref<PaymentResponse[]>([]);
const loading = ref(true);
const showPaid = ref(false);
const showProofModal = ref(false);
const selectedPayment = ref<PaymentResponse | null>(null);

const urgentPayments = computed(() =>
  [...payments.value]
    .filter(p => ['pending', 'overdue'].includes(p.status))
    .sort((a, b) => {
      if (a.status === 'overdue' && b.status !== 'overdue') return -1;
      if (b.status === 'overdue' && a.status !== 'overdue') return 1;
      return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
    })
);
const waitingPayments = computed(() =>
  payments.value.filter(p => p.status === 'waiting_confirmation')
    .sort((a, b) => new Date(b.due_date).getTime() - new Date(a.due_date).getTime())
);
const paidPayments = computed(() =>
  payments.value.filter(p => p.status === 'paid')
    .sort((a, b) => new Date(b.due_date).getTime() - new Date(a.due_date).getTime())
);

async function loadPayments() {
  loading.value = true;
  try { payments.value = await paymentsService.getTenantPayments(); }
  catch (err) { console.error(err); }
  finally { loading.value = false; }
}

function openProofModal(paymentId: number) {
  selectedPayment.value = payments.value.find(p => p.id === paymentId) || null;
  showProofModal.value = true;
}

function onProofSent() {
  showProofModal.value = false;
  selectedPayment.value = null;
  loadPayments();
}

onMounted(loadPayments);
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
.payments-section {
  margin-bottom: var(--space-10);
}

.payments-section--urgent {
  background: rgba(255, 255, 255, 0.32);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(185, 64, 64, 0.14);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: 0 -2px 0 var(--color-danger) inset;
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

.count-pill--info {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.count-pill--success {
  background: var(--color-success-bg);
  color: var(--color-success);
}

/* ---- Шапка колонок ---- */
.list-header {
  display: grid;
  /* 3px полоска + gap + дата + gap + статус + gap + сумма + gap + кнопка */
  grid-template-columns: 52px 1fr auto 140px;
  gap: var(--space-4);
  padding: 0 var(--space-5) var(--space-2) calc(3px + var(--space-4) + 52px + var(--space-4));
}

.list-header>div {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--color-dark-35);
}

.lh-amount {
  text-align: right;
}

/* ---- Список ---- */
.payments-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.payments-list--collapsed {
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