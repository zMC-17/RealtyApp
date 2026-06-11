<!-- pages/landlord/properties.vue -->
<template>
  <div class="content-page">
    <div class="content-inner">

      <header class="page-header">
        <div>
          <p class="page-eyebrow">Недвижимость</p>
          <h1 class="page-title">
            Объекты
            <span v-if="propertiesStore.propertiesCount > 0" class="title-count">
              {{ propertiesStore.propertiesCount }} {{ getObjectsWord(propertiesStore.propertiesCount) }}
            </span>
          </h1>
        </div>
        <button v-if="propertiesStore.hasProperties" class="btn-dark" @click="showCreateModal = true">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
          </svg>
          Добавить объект
        </button>
      </header>

      <!-- Лоадер -->
      <div v-if="propertiesStore.loading" class="loader-wrap">
        <div class="loader-line"></div>
        <p class="loader-label">Загрузка объектов…</p>
      </div>

      <!-- Ошибка -->
      <div v-else-if="propertiesStore.error" class="empty-state">
        <div class="empty-icon-box">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.4"/>
            <path d="M10 6v5M10 13v1" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
        </div>
        <p class="empty-title">Ошибка загрузки</p>
        <p class="empty-text">{{ propertiesStore.error }}</p>
        <button class="btn-ghost" @click="loadProperties">Попробовать снова</button>
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
        />
      </div>

    </div>
  </div>

  <CreatePropertyModal
    :visible="showCreateModal"
    @close="showCreateModal = false"
    @created="onPropertyCreated"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePropertiesStore } from '../../stores/properties';
import PropertyCard        from '../../components/properties/PropertyCard.vue';
import EmptyState          from '../../components/properties/EmptyState.vue';
import CreatePropertyModal from '../../components/properties/CreatePropertyModal.vue';

const propertiesStore = usePropertiesStore();
const showCreateModal  = ref(false);

onMounted(loadProperties);

async function loadProperties() { await propertiesStore.fetchProperties(); }
function onPropertyCreated() {}

function getObjectsWord(count: number) {
  const d = count % 10, dd = count % 100;
  if (dd >= 11 && dd <= 19) return 'объектов';
  if (d === 1) return 'объект';
  if (d >= 2 && d <= 4) return 'объекта';
  return 'объектов';
}
</script>

<style scoped>
.page-header {
  display: flex; align-items: flex-end; justify-content: space-between;
  margin-bottom: var(--space-8);
}
.page-eyebrow {
  font-size: var(--text-xs); font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--color-dark-35); margin-bottom: var(--space-1);
}
.page-title {
  font-size: var(--text-3xl); font-weight: 800; color: var(--color-dark);
  letter-spacing: -0.03em; line-height: 1;
  display: flex; align-items: baseline; gap: var(--space-3);
}
.title-count {
  font-size: var(--text-base); font-weight: 500; color: var(--color-dark-35);
}

.btn-dark {
  display: inline-flex; align-items: center; gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: var(--color-dark); color: var(--color-bg);
  border: none; border-radius: var(--radius-md);
  font-family: var(--font-base); font-size: var(--text-sm);
  font-weight: 600; cursor: pointer; transition: all var(--transition);
}
.btn-dark:hover {
  background: #2d2b27;
  box-shadow: 0 4px 16px rgba(28,26,23,0.20);
  transform: translateY(-1px);
}

.btn-ghost {
  display: inline-flex; align-items: center; gap: var(--space-2);
  padding: var(--space-2) var(--space-5); margin-top: var(--space-2);
  background: rgba(255,255,255,0.50); border: 1px solid rgba(255,255,255,0.65);
  border-radius: var(--radius-md); color: var(--color-dark-60);
  font-family: var(--font-base); font-size: var(--text-sm);
  font-weight: 500; cursor: pointer; transition: all var(--transition);
  backdrop-filter: blur(8px);
}
.btn-ghost:hover { background: rgba(255,255,255,0.70); color: var(--color-dark); }

/* Лоадер */
.loader-wrap {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--space-4); padding: var(--space-16);
}
.loader-line {
  width: 160px; height: 2px; background: rgba(28,26,23,0.10);
  border-radius: 1px; overflow: hidden; position: relative;
}
.loader-line::after {
  content: ''; position: absolute; inset: 0;
  background: var(--color-emerald);
  animation: loader 1.4s ease-in-out infinite;
}
@keyframes loader { 0% { transform: translateX(-100%); } 100% { transform: translateX(200%); } }
.loader-label { font-size: var(--text-sm); color: var(--color-dark-35); }

/* Пустое состояние (ошибка) */
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--space-3); padding: var(--space-16) var(--space-8); text-align: center;
}
.empty-icon-box {
  width: 52px; height: 52px; border-radius: var(--radius-lg);
  background: rgba(255,255,255,0.52); border: 1px solid rgba(255,255,255,0.65);
  backdrop-filter: blur(12px); display: flex; align-items: center; justify-content: center;
  margin-bottom: var(--space-2); color: var(--color-dark-35);
}
.empty-title { font-size: var(--text-lg); font-weight: 700; color: var(--color-dark); letter-spacing: -0.02em; }
.empty-text  { font-size: var(--text-sm); color: var(--color-dark-35); max-width: 300px; }

/* Сетка */
.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-5);
}
</style>