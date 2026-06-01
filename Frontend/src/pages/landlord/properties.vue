<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Объекты недвижимости"
    description="Mock-реализация управления объектами удалена. Этот экран будет заново подключаться к GET /properties/me, POST /properties и операциям редактирования/удаления."
    :bullets="[
      'Нужно вывести реальные объекты текущего пользователя.',
      'Форма создания и редактирования будет строиться поверх backend DTO.',
      'Здесь потом появятся фильтры, статусы и действия CRUD.'
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
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  font-size: 1.625rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.2;
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

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
}

.property-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.card-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.6rem;
}

.card-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.35;
  color: #111827;
}

.card-address {
  margin: 0;
  font-size: 0.85rem;
  color: #6b7280;
}

.card-description {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.45;
  color: #374151;
}

.card-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

:deep(.property-card .p-card-body) {
  padding: 0.85rem 0.9rem 0.8rem;
  gap: 0.65rem;
}

:deep(.property-card .p-card-content) {
  padding: 0;
}

:deep(.property-card .p-card-footer) {
  padding-top: 0.2rem;
}

@media (max-width: 1280px) {
  .cards-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
