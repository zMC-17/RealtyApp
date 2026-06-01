<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Договоры аренды"
    description="Mock-список договоров удалён. Этот экран будет заново собираться на базе GET /contracts/me, GET /contracts/owner/me, GET /contracts/tenant/me и POST /contracts."
    :bullets="[
      'Нужно отдельно показать договоры владельца и арендатора.',
      'Создание договора должно опираться на реальные property_id и tenant_id.',
      'Здесь позже появятся статусы, даты и управление договором.'
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
