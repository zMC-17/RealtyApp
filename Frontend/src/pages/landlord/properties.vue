<!-- pages/landlord/properties.vue -->
<template>
  <div class="properties-page">
    <!-- Заголовок и кнопка создания -->
    <div class="page-header">
      <div class="header-info">
        <h1>Мои объекты</h1>
        <span v-if="propertiesStore.propertiesCount > 0" class="count-badge">
          {{ propertiesStore.propertiesCount }}
          {{ getObjectsWord(propertiesStore.propertiesCount) }}
        </span>
      </div>

      <button
        v-if="propertiesStore.hasProperties"
        class="add-property-btn"
        @click="showCreateModal = true"
      >
        + Добавить объект
      </button>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="propertiesStore.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка объектов...</p>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-else-if="propertiesStore.error" class="error-state">
      <p>{{ propertiesStore.error }}</p>
      <button @click="loadProperties">Попробовать снова</button>
    </div>

    <!-- Пустое состояние -->
    <EmptyState
      v-else-if="!propertiesStore.hasProperties"
      @create="showCreateModal = true"
    />

    <!-- Сетка карточек -->
    <div v-else class="properties-grid">
      <PropertyCard
        v-for="property in propertiesStore.properties"
        :key="property.id"
        :property="property"
        @click="openPropertyDetails"
      />
    </div>

    <!-- Модальное окно создания -->
    <CreatePropertyModal
      :visible="showCreateModal"
      @close="showCreateModal = false"
      @created="onPropertyCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePropertiesStore } from '../../stores/properties';
import PropertyCard from '../../components/properties/PropertyCard.vue';
import EmptyState from '../../components/properties/EmptyState.vue';
import CreatePropertyModal from '../../components/properties/CreatePropertyModal.vue';

const propertiesStore = usePropertiesStore();
const showCreateModal = ref(false);

/**
 * Загрузить список объектов при монтировании
 */
onMounted(() => {
  loadProperties();
});

/**
 * Загрузка объектов
 */
const loadProperties = async () => {
  await propertiesStore.fetchProperties();
};

/**
 * Открыть детали объекта (пока редирект, потом будет страница)
 */
const openPropertyDetails = (propertyId: number) => {
  // В будущем: router.push({ name: 'PropertyDetails', params: { id: propertyId } })
  console.log('Открыть объект:', propertyId);
};

/**
 * Обработчик успешного создания объекта
 */
const onPropertyCreated = () => {
  console.log('Объект успешно создан');
};

/**
 * Склонение слова "объект" (русский язык)
 */
const getObjectsWord = (count: number): string => {
  const lastDigit = count % 10;
  const lastTwoDigits = count % 100;

  if (lastTwoDigits >= 11 && lastTwoDigits <= 19) return 'объектов';
  if (lastDigit === 1) return 'объект';
  if (lastDigit >= 2 && lastDigit <= 4) return 'объекта';
  return 'объектов';
};
</script>

<style scoped>
.properties-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  background:
    radial-gradient(circle at top left, rgba(168, 85, 247, 0.18), transparent 32%),
    radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.16), transparent 30%),
    linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-info h1 {
  margin: 0;
  font-size: 1.75rem;
  color: #2d3748;
}

.count-badge {
  background: #edf2f7;
  color: #4a5568;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.add-property-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.add-property-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.loading-state,
.error-state {
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
  border: 4px solid #e2e8f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #a0aec0;
  margin: 0;
}

.error-state p {
  color: #c53030;
  margin: 0 0 1rem 0;
}

.error-state button {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}
</style>