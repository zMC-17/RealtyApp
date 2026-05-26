<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Договоры аренды</h1>
        <p>Список действующих и ожидающих договоров</p>
      </div>

      <Button
        label="Создать договор"
        severity="contrast"
        size="small"
        @click="openCreateDialog"
      />
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка договоров...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="contractItems.length === 0" class="state state-empty">
      <h2>Договоров пока нет</h2>
      <p>Создайте первый договор для привязки арендатора к объекту.</p>
      <Button
        label="Создать договор"
        size="small"
        @click="openCreateDialog"
      />
    </div>

    <div v-else class="contracts-list">
      <Card
        v-for="item in contractItems"
        :key="item.id"
        class="contract-card"
      >
        <template #content>
          <div class="contract-row">
            <div class="contract-main">
              <div class="line-title">
                <span class="property-title">{{ item.propertyTitle }}</span>
                <Tag :value="item.statusLabel" :severity="item.statusSeverity" />
              </div>

              <div class="line-meta">
                <span>Арендатор: {{ item.tenantUsername }}</span>
                <span>{{ item.startDate }} - {{ item.endDate }}</span>
              </div>
            </div>

            <div class="payment-block">
              <span class="payment-label">Ежемесячно</span>
              <strong>{{ item.monthlyPayment }}</strong>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <ContractDialog
      v-model:visible="isDialogVisible"
      :loading="isDialogLoading"
      :property-options="propertyOptions"
      :tenant-options="tenantOptions"
      @submit="handleCreateContract"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Tag from 'primevue/tag';
import type { ContractStatus } from '../../shared/types';
import { createContract, getContractsByOwner } from '../../services/mock/contracts';
import { getPropertyById, getPropertiesByOwner } from '../../services/mock/properties';
import { getTenants, getUsersByIds } from '../../services/mock/users';
import { useAuthStore } from '../../stores/auth';
import ContractDialog from '../../components/contract/ContractDialog.vue';

type TagSeverity = 'secondary' | 'info' | 'success' | 'warn' | 'danger' | 'contrast';

interface ContractItem {
  id: string;
  propertyTitle: string;
  tenantUsername: string;
  startDate: string;
  endDate: string;
  monthlyPayment: string;
  statusLabel: string;
  statusSeverity: TagSeverity;
}

interface SelectOption {
  label: string;
  value: string;
}

interface ContractFormPayload {
  property_id: string;
  tenant_id: string;
  start_date: string;
  end_date: string;
  monthly_payment: number;
}

const authStore = useAuthStore();

const contractItems = ref<ContractItem[]>([]);
const isLoading = ref(false);
const errorMessage = ref('');
const isDialogVisible = ref(false);
const isDialogLoading = ref(false);
const propertyOptions = ref<SelectOption[]>([]);
const tenantOptions = ref<SelectOption[]>([]);

const getOwnerId = (): string => authStore.user?.id ?? 'user_1';

const formatDate = (dateValue: string): string => {
  const date = new Date(dateValue);
  return date.toLocaleDateString('ru-RU');
};

const formatMoney = (value: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0,
  }).format(value);
};

const statusMeta = (status: ContractStatus): { label: string; severity: TagSeverity } => {
  if (status === 'active') {
    return { label: 'Активен', severity: 'success' };
  }

  if (status === 'pending') {
    return { label: 'Ожидает', severity: 'warn' };
  }

  return { label: 'Расторгнут', severity: 'secondary' };
};

const loadContracts = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const ownerId = getOwnerId();
    const contracts = await getContractsByOwner(ownerId);

    const tenantIds = [...new Set(contracts.map(contract => contract.tenant_id))];
    const tenants = await getUsersByIds(tenantIds);
    const tenantMap = new Map(tenants.map(user => [user.id, user.username]));

    const propertyTitlePairs = await Promise.all(
      contracts.map(async contract => {
        const property = await getPropertyById(contract.property_id);
        return [contract.property_id, property?.title ?? 'Неизвестный объект'] as const;
      })
    );
    const propertyMap = new Map(propertyTitlePairs);

    contractItems.value = contracts.map(contract => {
      const status = statusMeta(contract.status);
      return {
        id: contract.id,
        propertyTitle: propertyMap.get(contract.property_id) ?? 'Неизвестный объект',
        tenantUsername: tenantMap.get(contract.tenant_id) ?? contract.tenant_id,
        startDate: formatDate(contract.start_date),
        endDate: formatDate(contract.end_date),
        monthlyPayment: formatMoney(contract.monthly_payment),
        statusLabel: status.label,
        statusSeverity: status.severity,
      };
    });
  } catch {
    errorMessage.value = 'Не удалось загрузить договоры. Попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

const loadDialogOptions = async () => {
  const ownerId = getOwnerId();
  const [ownerProperties, tenants] = await Promise.all([
    getPropertiesByOwner(ownerId),
    getTenants(),
  ]);

  propertyOptions.value = ownerProperties.map(property => ({
    label: property.title,
    value: property.id,
  }));

  tenantOptions.value = tenants.map(tenant => ({
    label: tenant.username,
    value: tenant.id,
  }));
};

const openCreateDialog = async () => {
  errorMessage.value = '';
  isDialogLoading.value = true;

  try {
    await loadDialogOptions();

    if (propertyOptions.value.length === 0) {
      errorMessage.value = 'Сначала добавьте хотя бы один объект недвижимости.';
      return;
    }

    if (tenantOptions.value.length === 0) {
      errorMessage.value = 'Нет доступных арендаторов для создания договора.';
      return;
    }

    isDialogVisible.value = true;
  } catch {
    errorMessage.value = 'Не удалось подготовить форму договора. Попробуйте снова.';
  } finally {
    isDialogLoading.value = false;
  }
};

const handleCreateContract = async (payload: ContractFormPayload) => {
  isDialogLoading.value = true;
  errorMessage.value = '';

  try {
    await createContract({
      property_id: payload.property_id,
      tenant_id: payload.tenant_id,
      start_date: payload.start_date,
      end_date: payload.end_date,
      monthly_payment: payload.monthly_payment,
      status: 'pending',
    });

    isDialogVisible.value = false;
    await loadContracts();
  } catch {
    errorMessage.value = 'Не удалось создать договор. Попробуйте снова.';
  } finally {
    isDialogLoading.value = false;
  }
};

onMounted(loadContracts);
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
  margin: 0.45rem 0 0.9rem;
}

.state-error {
  border-color: #fecaca;
  background: #fef2f2;
  color: #991b1b;
}

.contracts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.contract-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.contract-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.contract-main {
  min-width: 0;
  flex: 1;
}

.line-title {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-bottom: 0.45rem;
}

.property-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.line-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #6b7280;
  font-size: 0.88rem;
  flex-wrap: wrap;
}

.payment-block {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.15rem;
  white-space: nowrap;
}

.payment-label {
  font-size: 0.78rem;
  color: #6b7280;
}

.payment-block strong {
  font-size: 1rem;
  color: #111827;
}

:deep(.contract-card .p-card-body) {
  padding: 0.75rem 0.9rem;
}

:deep(.contract-card .p-card-content) {
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

  .contract-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .payment-block {
    align-items: flex-start;
  }
}
</style>
