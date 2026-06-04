<!-- pages/landlord/payments.vue -->
<template>
  <div class="payments-page">
    <div class="page-header">
      <h1>Платежи</h1>
      <button class="refresh-btn" @click="loadPayments" :disabled="paymentsStore.loading">
        🔄 Обновить
      </button>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="paymentsStore.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка платежей...</p>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-else-if="paymentsStore.error" class="error-state">
      <p>{{ paymentsStore.error }}</p>
      <button @click="loadPayments">Попробовать снова</button>
    </div>

    <template v-else>
      <!-- Секция: Требуют внимания -->
      <section v-if="paymentsStore.hasAttentionPayments" class="section section--attention">
        <h2 class="section-title">
          <span class="section-icon">⚠️</span>
          Требуют внимания
          <span class="count-badge count-badge--attention">
            {{ paymentsStore.attentionPayments.length }}
          </span>
        </h2>

        <div class="payments-grid">
          <PaymentCard v-for="payment in paymentsStore.attentionPayments" :key="payment.id" :payment="payment"
            @confirm="openConfirmModal" @reject="handleReject" />
        </div>
      </section>

      <!-- Секция: Ближайшие платежи -->
      <section v-if="paymentsStore.upcomingPayments.length > 0" class="section">
        <h2 class="section-title">
          <span class="section-icon">📅</span>
          Ближайшие платежи
          <span class="count-badge">
            {{ paymentsStore.upcomingPayments.length }}
          </span>
        </h2>

        <div class="payments-grid">
          <PaymentCard v-for="payment in paymentsStore.upcomingPayments" :key="payment.id" :payment="payment" />
        </div>
      </section>

      <!-- Пустое состояние -->
      <div v-if="!paymentsStore.hasAttentionPayments && paymentsStore.upcomingPayments.length === 0"
        class="empty-state">
        <div class="empty-icon">💰</div>
        <h2>Платежей пока нет</h2>
        <p>Здесь будут отображаться платежи по вашим объектам</p>
      </div>
    </template>

    <!-- Модальное окно подтверждения -->
    <ConfirmPaymentModal :visible="showConfirmModal" :payment="selectedPayment" @close="closeConfirmModal"
      @confirmed="onPaymentConfirmed" />
  </div>
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

onMounted(() => {
  loadPayments();
});

const loadPayments = async () => {
  await paymentsStore.fetchPayments();
};

const openConfirmModal = (paymentId: number) => {
  selectedPayment.value = paymentsStore.payments.find(p => p.id === paymentId) || null;
  showConfirmModal.value = true;
};

const closeConfirmModal = () => {
  showConfirmModal.value = false;
  selectedPayment.value = null;
};

const handleReject = async (paymentId: number) => {
  await paymentsStore.rejectPayment(paymentId);
};

const onPaymentConfirmed = () => {
  // Платёж подтверждён, список обновлён в store
};
</script>

<style scoped>
.payments-page {
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
  transition: background 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #e5e7eb;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.section {
  margin-bottom: 2.5rem;
}

.section--attention {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.section-icon {
  font-size: 1.5rem;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.5rem;
  background: #e5e7eb;
  color: #374151;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.count-badge--attention {
  background: #ef4444;
  color: white;
  animation: pulse 2s infinite;
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }
}

.payments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1rem;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p,
.error-state p {
  color: #6b7280;
}

.error-state button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h2 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.empty-state p {
  color: #6b7280;
}
</style>