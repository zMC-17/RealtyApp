<!-- pages/tenant/dashboard.vue -->
<template>
  <div class="tenant-dashboard">
    <!-- Индикатор загрузки -->
    <div v-if="tenantStore.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка данных...</p>
    </div>

    <!-- Ошибка -->
    <div v-else-if="tenantStore.error" class="error-state">
      <p>{{ tenantStore.error }}</p>
      <button @click="loadData">Попробовать снова</button>
    </div>

    <template v-else>
      <!-- Ожидающие подтверждения договоры -->
      <section v-if="tenantStore.hasPendingContracts" class="section section--pending">
        <h2 class="section-title">
          <span class="section-icon">📨</span>
          Приглашение в договор
        </h2>
        <p class="section-description">
          Владелец приглашает вас в договор аренды. Подтвердите участие или отклоните.
        </p>

        <div class="pending-contracts">
          <PendingContractCard v-for="contract in tenantStore.pendingContracts" :key="contract.id" :contract="contract"
            @confirm="handleConfirm" />
        </div>
      </section>

      <!-- Активный договор -->
      <section v-if="tenantStore.hasActiveContract" class="section">
        <h2 class="section-title">
          <span class="section-icon">📋</span>
          Мой договор
        </h2>

        <ActiveContractCard :contract="tenantStore.activeContract!" />

        <!-- Быстрая информация -->
        <QuickInfo :contract="tenantStore.activeContract!" />
      </section>

      <!-- Нет договоров -->
      <div v-if="!tenantStore.hasPendingContracts && !tenantStore.hasActiveContract" class="empty-state">
        <div class="empty-icon">📭</div>
        <h2>У вас пока нет договоров</h2>
        <p>Когда владелец добавит вас в договор аренды, он появится здесь</p>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useTenantStore } from '../../stores/tenant';
import PendingContractCard from '../../components/tenant/PendingContractCard.vue';
import ActiveContractCard from '../../components/tenant/ActiveContractCard.vue';
import QuickInfo from '../../components/tenant/QuickInfo.vue';

const tenantStore = useTenantStore();

const loadData = () => tenantStore.fetchContracts();

const handleConfirm = async (contractId: number) => {
  await tenantStore.confirmContract(contractId);
};

onMounted(loadData);
</script>

<style scoped>
.tenant-dashboard {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
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

.error-state p {
  color: #dc2626;
  margin-bottom: 1rem;
}

.error-state button {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.section {
  margin-bottom: 2rem;
}

.section--pending {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 12px;
  padding: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.section-icon {
  font-size: 1.5rem;
}

.section-description {
  color: #92400e;
  margin: 0 0 1.5rem 0;
}

.pending-contracts {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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