<!-- pages/tenant/payments.vue -->
<template>
  <div class="tenant-payments">
    <div class="page-header">
      <h1>Платежи</h1>
      <button class="refresh-btn" @click="loadPayments" :disabled="loading">
        🔄 Обновить
      </button>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка платежей...</p>
    </div>

    <!-- Пустое состояние -->
    <div v-else-if="payments.length === 0" class="empty-state">
      <div class="empty-icon">💰</div>
      <h2>Платежей пока нет</h2>
      <p>Платежи появятся после активации договора</p>
    </div>

    <template v-else>
      <!-- Требуют оплаты: просроченные + все pending -->
      <section v-if="urgentPayments.length > 0" class="section">
        <h2 class="section-title section-title--urgent">
          <span>⚠️</span> Требуют оплаты
          <span class="count-badge count-badge--urgent">{{ urgentPayments.length }}</span>
        </h2>
        <div class="payments-list">
          <TenantPaymentCard v-for="payment in urgentPayments" :key="payment.id" :payment="payment"
            @send-proof="openProofModal" />
        </div>
      </section>

      <!-- На подтверждении -->
      <section v-if="waitingPayments.length > 0" class="section">
        <h2 class="section-title section-title--waiting">
          <span>🔍</span> На подтверждении
          <span class="count-badge count-badge--waiting">{{ waitingPayments.length }}</span>
        </h2>
        <div class="payments-list">
          <TenantPaymentCard v-for="payment in waitingPayments" :key="payment.id" :payment="payment" />
        </div>
      </section>

      <!-- Оплаченные (сворачиваемые) -->
      <section v-if="paidPayments.length > 0" class="section">
        <button class="collapse-btn" @click="showPaid = !showPaid">
          <span>{{ showPaid ? '🟢' : '▶️' }}</span>
          Оплаченные
          <span class="count-badge count-badge--paid">{{ paidPayments.length }}</span>
        </button>
        <div v-if="showPaid" class="payments-list">
          <TenantPaymentCard v-for="payment in paidPayments" :key="payment.id" :payment="payment" />
        </div>
      </section>
    </template>

    <!-- Модалка отправки чека -->
    <RequestConfirmationModal v-if="showProofModal && selectedPayment" :visible="showProofModal"
      :payment="selectedPayment" @close="showProofModal = false" @sent="onProofSent" />
  </div>
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

// Требуют оплаты: просроченные + все pending (включая будущие)
const urgentPayments = computed(() =>
  [...payments.value]
    .filter(p => p.status === 'pending' || p.status === 'overdue')
    .sort((a, b) => {
      // Просроченные первее
      if (a.status === 'overdue' && b.status !== 'overdue') return -1;
      if (b.status === 'overdue' && a.status !== 'overdue') return 1;
      // Затем по дате (ближайшие сверху)
      return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
    })
);

// На подтверждении
const waitingPayments = computed(() =>
  payments.value
    .filter(p => p.status === 'waiting_confirmation')
    .sort((a, b) => new Date(b.due_date).getTime() - new Date(a.due_date).getTime())
);

// Оплаченные
const paidPayments = computed(() =>
  payments.value
    .filter(p => p.status === 'paid')
    .sort((a, b) => new Date(b.due_date).getTime() - new Date(a.due_date).getTime())
);

const loadPayments = async () => {
  loading.value = true;
  try {
    payments.value = await paymentsService.getTenantPayments();
  } catch (err) {
    console.error('Ошибка загрузки платежей:', err);
  } finally {
    loading.value = false;
  }
};

const openProofModal = (paymentId: number) => {
  selectedPayment.value = payments.value.find(p => p.id === paymentId) || null;
  showProofModal.value = true;
};

const onProofSent = () => {
  showProofModal.value = false;
  selectedPayment.value = null;
  loadPayments();
};

onMounted(loadPayments);
</script>

<style scoped>
.tenant-payments {
  padding: 2rem;
  max-width: 800px;
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
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: #1f2937;
  margin: 0 0 1rem 0;
}

.section-title--urgent {
  color: #dc2626;
}

.section-title--waiting {
  color: #2563eb;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.5rem;
  background: #e5e7eb;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
}

.count-badge--urgent {
  background: #fecaca;
  color: #dc2626;
}

.count-badge--waiting {
  background: #bfdbfe;
  color: #2563eb;
}

.count-badge--paid {
  background: #bbf7d0;
  color: #16a34a;
}

.payments-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.collapse-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  color: #374151;
  cursor: pointer;
  transition: background 0.2s;
}

.collapse-btn:hover {
  background: #f3f4f6;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 2rem;
  text-align: center;
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

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h2 {
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #6b7280;
}
</style>