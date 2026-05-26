<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Мои объекты</h1>
        <p>Управление недвижимостью владельца</p>
      </div>

      <Button
        label="Добавить объект"
        severity="contrast"
        size="small"
        @click="handleAddProperty"
      />
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка объектов...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="properties.length === 0" class="state state-empty">
      <h2>Пока нет объектов</h2>
      <p>Добавьте первый объект недвижимости, чтобы начать работу.</p>
      <Button
        label="Добавить объект"
        size="small"
        @click="handleAddProperty"
      />
    </div>

    <div v-else class="cards-grid">
      <Card
        v-for="property in properties"
        :key="property.id"
        class="property-card"
      >
        <template #title>
          <div class="card-title-row">
            <h3 class="card-title">{{ property.title }}</h3>
            <Tag
              :value="getPropertyStatus(property.id).label"
              :severity="getPropertyStatus(property.id).severity"
            />
          </div>
        </template>

        <template #subtitle>
          <p class="card-address">{{ property.address }}</p>
        </template>

        <template #content>
          <p class="card-description">
            {{ truncateDescription(property.description) }}
          </p>
        </template>

        <template #footer>
          <div class="card-actions">
            <Button
              label="Изменить"
              outlined
              size="small"
              @click="handleEditProperty(property.id)"
            />
            <Button
              label="Удалить"
              severity="danger"
              text
              size="small"
              @click="handleDeleteProperty(property.id)"
            />
          </div>
        </template>
      </Card>
    </div>

    <PropertyDialog
      v-model:visible="isDialogVisible"
      :mode="dialogMode"
      :loading="isDialogLoading"
      :initialValue="dialogInitialValue"
      @submit="handleDialogSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Tag from 'primevue/tag';
import type { Property } from '../../shared/types';
import {
  createProperty,
  deleteProperty,
  getPropertiesByOwner,
  updateProperty,
} from '../../services/mock/properties';
import { useAuthStore } from '../../stores/auth';
import PropertyDialog from '../../components/property/PropertyDialog.vue';

type TagSeverity = 'secondary' | 'info' | 'success' | 'warn' | 'danger' | 'contrast';

const authStore = useAuthStore();

const properties = ref<Property[]>([]);
const isLoading = ref(false);
const errorMessage = ref('');
const isDialogVisible = ref(false);
const isDialogLoading = ref(false);
const dialogMode = ref<'create' | 'edit'>('create');
const editingPropertyId = ref<string | null>(null);
const dialogInitialValue = ref<Pick<Property, 'title' | 'address' | 'description' | 'property_type'>>({
  title: '',
  address: '',
  description: '',
  property_type: 'apartment',
});

const getOwnerId = (): string => authStore.user?.id ?? 'user_1';

const loadProperties = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    properties.value = await getPropertiesByOwner(getOwnerId());
  } catch {
    errorMessage.value = 'Не удалось загрузить объекты. Попробуйте снова.';
  } finally {
    isLoading.value = false;
  }
};

const truncateDescription = (description: string): string => {
  if (description.length <= 90) return description;
  return `${description.slice(0, 90)}...`;
};

const getPropertyStatus = (propertyId: string): { label: string; severity: TagSeverity } => {
  const statuses: Array<{ label: string; severity: TagSeverity }> = [
    { label: 'Активен', severity: 'success' },
    { label: 'Черновик', severity: 'secondary' },
    { label: 'На проверке', severity: 'warn' },
  ];

  const hash = propertyId
    .split('')
    .reduce((acc, char) => acc + char.charCodeAt(0), 0);

  return statuses[hash % statuses.length];
};

const handleAddProperty = () => {
  dialogMode.value = 'create';
  editingPropertyId.value = null;
  dialogInitialValue.value = {
    title: '',
    address: '',
    description: '',
    property_type: 'apartment',
  };
  isDialogVisible.value = true;
};

const handleEditProperty = (propertyId: string) => {
  const property = properties.value.find(item => item.id === propertyId);
  if (!property) {
    errorMessage.value = 'Объект не найден для редактирования.';
    return;
  }

  dialogMode.value = 'edit';
  editingPropertyId.value = propertyId;
  dialogInitialValue.value = {
    title: property.title,
    address: property.address,
    description: property.description,
    property_type: property.property_type,
  };
  isDialogVisible.value = true;
};

const handleDialogSubmit = async (
  value: Pick<Property, 'title' | 'address' | 'description' | 'property_type'>
) => {
  isDialogLoading.value = true;
  errorMessage.value = '';

  try {
    if (dialogMode.value === 'create') {
      const created = await createProperty(getOwnerId(), value);
      properties.value = [created, ...properties.value];
    } else {
      if (!editingPropertyId.value) {
        errorMessage.value = 'Не удалось определить объект для обновления.';
        return;
      }

      const updated = await updateProperty(editingPropertyId.value, value);
      if (!updated) {
        errorMessage.value = 'Объект не найден или уже удалён.';
        return;
      }

      properties.value = properties.value.map(item =>
        item.id === updated.id ? updated : item
      );
    }

    isDialogVisible.value = false;
  } catch {
    errorMessage.value = 'Не удалось сохранить изменения. Попробуйте снова.';
  } finally {
    isDialogLoading.value = false;
  }
};

const handleDeleteProperty = async (propertyId: string) => {
  const confirmed = window.confirm('Удалить объект? Это действие нельзя отменить.');
  if (!confirmed) return;

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const deleted = await deleteProperty(propertyId);
    if (!deleted) {
      errorMessage.value = 'Объект не найден или уже удалён.';
      return;
    }

    properties.value = properties.value.filter(item => item.id !== propertyId);
  } catch {
    errorMessage.value = 'Ошибка удаления объекта. Попробуйте снова.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(loadProperties);
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
