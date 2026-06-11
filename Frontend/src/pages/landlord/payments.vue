<!-- pages/landlord/payments.vue -->
<template>
  <div class="content-page">
    <div class="content-inner">

      <header class="page-header">
        <div>
          <p class="page-eyebrow">Финансы</p>
          <h1 class="page-title">Платежи</h1>
        </div>
        <button class="btn-ghost" @click="loadPayments" :disabled="paymentsStore.loading">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"
            :style="{ animation: paymentsStore.loading ? 'spin 1s linear infinite' : 'none' }">
            <path d="M1.5 7A5.5 5.5 0 1 0 7 1.5a5.5 5.5 0 0 0-4.2 1.96" stroke="currentColor" stroke-width="1.4"
              stroke-linecap="round" />
            <path d="M1.5 1.5v3.5H5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
          Обновить
        </button>
      </header>

      <!-- Лоадер -->
      <div v-if="paymentsStore.loading" class="loader-wrap">
        <div class="loader-line"></div>
        <p class="loader-label">Загрузка платежей…</p>
      </div>

      <!-- Ошибка -->
      <div v-else-if="paymentsStore.error" class="empty-state">
        <div class="empty-icon-box">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.4" />
            <path d="M10 6v5M10 13v1" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
          </svg>
        </div>
        <p class="empty-title">Ошибка загрузки</p>
        <p class="empty-text">{{ paymentsStore.error }}</p>
        <button class="btn-ghost" @click="loadPayments">Попробовать снова</button>
      </div>

      <template v-else>

        <!-- Секция: требуют внимания -->
        <section v-if="paymentsStore.hasAttentionPayments" class="payments-section payments-section--attention">
          <div class="section-head">
            <h2 class="section-title">
              Требуют внимания
            </h2>
            <span class="count-pill count-pill--danger">{{ paymentsStore.attentionPayments.length }}</span>
          </div>

          <!-- Шапка колонок -->
          <div class="list-header">
            <div class="lh-status">Статус</div>
            <div class="lh-property">Объект</div>
            <div class="lh-tenant">Арендатор</div>
            <div class="lh-amount">Сумма</div>
            <div class="lh-actions"></div>
          </div>

          <div class="payments-list">
            <PaymentCard v-for="payment in paymentsStore.attentionPayments" :key="payment.id" :payment="payment"
              @confirm="openConfirmModal" @reject="handleReject" />
          </div>
        </section>

        <!-- Секция: ближайшие -->
        <section v-if="paymentsStore.upcomingPayments.length > 0" class="payments-section">
          <div class="section-head">
            <h2 class="section-title">Ближайшие платежи</h2>
            <span class="count-pill">{{ paymentsStore.upcomingPayments.length }}</span>
          </div>

          <div class="list-header">
            <div class="lh-status">Статус</div>
            <div class="lh-property">Объект</div>
            <div class="lh-tenant">Арендатор</div>
            <div class="lh-amount">Сумма</div>
            <div class="lh-actions"></div>
          </div>

          <div class="payments-list">
            <PaymentCard v-for="payment in paymentsStore.upcomingPayments" :key="payment.id" :payment="payment" />
          </div>
        </section>

        <!-- Пусто -->
        <div v-if="!paymentsStore.hasAttentionPayments && paymentsStore.upcomingPayments.length === 0"
          class="empty-state">
          <div class="empty-icon-box">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="2" y="5" width="16" height="12" rx="2" stroke="currentColor" stroke-width="1.4" />
              <path d="M2 9h16" stroke="currentColor" stroke-width="1.4" />
              <circle cx="5.5" cy="13" r="1" fill="currentColor" />
            </svg>
          </div>
          <p class="empty-title">Платежей пока нет</p>
          <p class="empty-text">Платежи появятся после создания договоров с арендаторами</p>
        </div>

      </template>
    </div>
  </div>

  <ConfirmPaymentModal :visible="showConfirmModal" :payment="selectedPayment" @close="closeConfirmModal"
    @confirmed="onPaymentConfirmed" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePaymentsStore } from '../../stores/payments';
import type { PaymentResponse } from '../../types/payment';
import PaymentCard from '../../components/payments/PaymentCard.vue';
import ConfirmPaymentModal from '../../components/payments/ConfirmPaymentModal.vue';

const paymentsStore = usePaymentsStore();
const showConfirmModal = ref(false);
const selectedPayment = ref<PaymentResponse | null>(null);

onMounted(loadPayments);

async function loadPayments() { await paymentsStore.fetchPayments(); }

function openConfirmModal(paymentId: number) {
  selectedPayment.value = paymentsStore.payments.find(p => p.id === paymentId) || null;
  showConfirmModal.value = true;
}

function closeConfirmModal() {
  showConfirmModal.value = false;
  selectedPayment.value = null;
}

async function handleReject(paymentId: number) {
  await paymentsStore.rejectPayment(paymentId);
}

function onPaymentConfirmed() { }
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
.payments-section {
  margin-bottom: var(--space-10);
}

.payments-section--attention {
  background: rgba(255, 255, 255, 0.32);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(185, 64, 64, 0.14);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  /* Тонкий верхний акцент — опасность */
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

/* ---- Шапка колонок ---- */
.list-header {
  display: grid;
  grid-template-columns: 160px 1fr 1fr auto 72px;
  gap: var(--space-4);
  padding: 0 var(--space-5) var(--space-2) calc(var(--space-5) + 3px + var(--space-4));
  /* 3px = ширина accent-полоски + gap */
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
</style>