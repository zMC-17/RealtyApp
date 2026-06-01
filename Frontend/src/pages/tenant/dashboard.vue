<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Панель арендатора"
    description="Mock-dashboard удалён. Этот экран будет собирать состояние договора, платежей и заявок только после подключения реального backend API."
    :bullets="[
      'Понадобятся данные по активному договору арендатора.',
      'Платежи и заявки нужно будет загружать без mock-фильтров.',
      'Это должна быть сводная панель, а не набор локально подделанных данных.'
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
  overflow-y: auto;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
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
  min-height: 300px;
  padding: 2rem;
  color: #4b5563;
}

.state-loading {
  background: #f9fafb;
}

.state-error {
  border-color: #fecaca;
  background: #fef2f2;
  color: #991b1b;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.section-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.75rem;
  height: 1.75rem;
  background: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
}

/* Contract Card */
.contract-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.contract-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.contract-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contract-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.contract-item strong {
  font-size: 0.95rem;
  color: #111827;
  word-break: break-word;
}

.amount {
  font-size: 1rem;
  color: #1e40af;
  font-weight: 700;
}

/* Payments List */
.payments-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.payment-item {
  border: 1px solid #e5e7eb;
  border-radius: 0.6rem;
}

.payment-grid {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  align-items: center;
  gap: 1rem;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.payment-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.payment-info strong {
  font-size: 0.9rem;
  color: #111827;
}

.payment-status {
  display: flex;
  justify-content: flex-end;
}

/* Requests List */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.request-item {
  border: 1px solid #e5e7eb;
  border-radius: 0.6rem;
}

.request-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1rem;
  align-items: flex-start;
}

.request-info {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.request-message {
  margin: 0;
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.4;
  word-break: break-word;
}

.request-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.request-date {
  font-size: 0.75rem;
  color: #9ca3af;
}

.request-status {
  display: flex;
  justify-content: flex-end;
}

.empty-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 120px;
  border: 1px dashed #e5e7eb;
  border-radius: 0.75rem;
  background: #f9fafb;
  color: #9ca3af;
  text-align: center;
  padding: 1rem;
}

.empty-state p {
  margin: 0;
  font-size: 0.9rem;
}

/* PrimeVue Overrides */
:deep(.contract-card .p-card-body) {
  padding: 1rem 1.1rem;
}

:deep(.contract-card .p-card-content) {
  padding: 0;
}

:deep(.payment-item .p-card-body) {
  padding: 0.75rem 1rem;
}

:deep(.payment-item .p-card-content) {
  padding: 0;
}

:deep(.request-item .p-card-body) {
  padding: 0.75rem 1rem;
}

:deep(.request-item .p-card-content) {
  padding: 0;
}

:deep(.p-tag) {
  font-size: 0.7rem;
  padding: 0.35rem 0.65rem;
}

/* Responsive */
@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .contract-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .payment-grid {
    grid-template-columns: 1fr auto;
  }

  .request-grid {
    grid-template-columns: 1fr;
  }

  .request-status {
    justify-content: flex-start;
  }
}

@media (max-width: 640px) {
  .page-container {
    padding: 0.75rem;
  }

  .contract-grid {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 1.35rem;
  }
}
</style>
