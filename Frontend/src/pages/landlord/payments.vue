<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Платежи"
    description="Mock-реализация платежей удалена. Этот экран будет заново подключаться к GET /payments/me, GET /payments/owner/me, GET /payments/tenant/me и GET /payments/contracts/{contract_id}."
    :bullets="[
      'Нужно показывать платежи по владельцу и по договору.',
      'Статусы и суммы должны приходить из backend DTO.',
      'Фильтры и действия добавятся после подключения API.'
    ]"
  />
</template>

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

.filters {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 180px;
}

.filters label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #4b5563;
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

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filters {
    min-width: 0;
  }
}
</style>
