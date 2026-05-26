<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Мои платежи</h1>
        <p>Текущие обязательства по оплате аренды</p>
      </div>
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка платежей...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="paymentItems.length === 0" class="state state-empty">
      <h2>Платежей пока нет</h2>
      <p>Обязательства появятся после создания активного договора.</p>
    </div>

    <div v-else class="payments-list">
      <Card
        v-for="item in paymentItems"
        :key="item.id"
        class="payment-card"
      >
        <template #content>
          <div class="payment-row">
            <div class="payment-main">
              <div class="line-title">
                <strong>{{ item.amount }}</strong>
                <Tag :value="item.statusLabel" :severity="item.statusSeverity" />
              </div>

              <div class="line-meta">
                <span>Срок оплаты: {{ item.dueDate }}</span>
                <span>Договор: {{ item.contractCode }}</span>
              </div>
            </div>

            <div class="payment-actions">
              <Button
                v-if="item.status === 'unpaid'"
                label="Mark as Paid"
                size="small"
                @click="handleMarkAsPaid(item.id)"
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
import Button from 'primevue/button';
import Card from 'primevue/card';
import Tag from 'primevue/tag';
import type { PaymentStatus } from '../../shared/types';
import { getContractsByTenant } from '../../services/mock/contracts';
import { getPaymentsByContract, markPaymentAsPaid } from '../../services/mock/payments';
import { useAuthStore } from '../../stores/auth';

type TagSeverity = 'secondary' | 'info' | 'success' | 'warn' | 'danger' | 'contrast';

interface TenantPaymentItem {
  id: string;
  contractCode: string;
  amount: string;
  dueDate: string;
  dueDateRaw: string;
  status: PaymentStatus;
  statusLabel: string;
  statusSeverity: TagSeverity;
}

const authStore = useAuthStore();

const paymentItems = ref<TenantPaymentItem[]>([]);
const isLoading = ref(false);
const errorMessage = ref('');

const getTenantId = (): string => authStore.user?.id ?? 'user_3';

const formatDate = (value: string): string => new Date(value).toLocaleDateString('ru-RU');

const formatMoney = (value: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0,
  }).format(value);
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

const loadPayments = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const tenantContracts = await getContractsByTenant(getTenantId());

    const nestedPayments = await Promise.all(
      tenantContracts.map(async contract => {
        const payments = await getPaymentsByContract(contract.id);

        return payments.map(payment => {
          const status = statusMeta(payment.status);

          return {
            id: payment.id,
            contractCode: contract.id,
            amount: formatMoney(payment.amount),
            dueDate: formatDate(payment.due_date),
            dueDateRaw: payment.due_date,
            status: payment.status,
            statusLabel: status.label,
            statusSeverity: status.severity,
          } satisfies TenantPaymentItem;
        });
      })
    );

    paymentItems.value = nestedPayments
      .flat()
      .sort((a, b) => new Date(a.dueDateRaw).getTime() - new Date(b.dueDateRaw).getTime());
  } catch {
    errorMessage.value = 'Не удалось загрузить платежи. Попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

const handleMarkAsPaid = async (paymentId: string) => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const updated = await markPaymentAsPaid(paymentId);
    if (!updated) {
      errorMessage.value = 'Платёж не найден.';
      return;
    }

    await loadPayments();
  } catch {
    errorMessage.value = 'Не удалось обновить статус платежа.';
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

.payment-actions {
  display: flex;
  align-items: center;
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

  .payment-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
