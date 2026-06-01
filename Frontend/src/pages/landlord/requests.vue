<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Заявки от арендаторов"
    description="Mock-логика заявок удалена. Этот экран будет заново подключаться к GET /requests/me, GET /requests/owner/me, GET /requests/tenant/me и GET /requests/contracts/{contract_id}."
    :bullets="[
      'Владелец должен видеть обращения по своим объектам.',
      'Изменение статуса заявки будет работать через backend.',
      'Фильтры и действия появятся после подключения API.'
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
  margin: 0.45rem 0 0;
}

.state-error {
  border-color: #fecaca;
  background: #fef2f2;
  color: #991b1b;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.request-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.request-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.9rem;
}

.request-main {
  min-width: 0;
  flex: 1;
}

.message {
  margin: 0 0 0.55rem;
  color: #111827;
  font-size: 0.95rem;
  line-height: 1.45;
}

.meta-line {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  flex-wrap: wrap;
  color: #6b7280;
  font-size: 0.84rem;
}

.status-control {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 170px;
}

.status-control label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #4b5563;
}

:deep(.request-card .p-card-body) {
  padding: 0.72rem 0.9rem;
}

:deep(.request-card .p-card-content) {
  padding: 0;
}

@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .request-row {
    flex-direction: column;
  }

  .status-control {
    min-width: 0;
    width: 100%;
  }
}
</style>
