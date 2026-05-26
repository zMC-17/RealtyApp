<template>
  <Dialog
    :visible="visible"
    :modal="true"
    :draggable="false"
    :closable="!loading"
    :style="{ width: '34rem' }"
    :content-style="{ backgroundColor: 'white' }"
    :breakpoints="{ '960px': '92vw' }"
    @update:visible="handleDialogVisibility"
  >
    <template #header>
      <div class="dialog-header">
        <h3>{{ mode === 'edit' ? 'Редактирование объекта' : 'Новый объект' }}</h3>
      </div>
    </template>

    <form class="form-grid" @submit.prevent="handleSubmit">
      <div class="field">
        <label for="property-title">Название</label>
        <InputText
          id="property-title"
          v-model="form.title"
          fluid
          :invalid="Boolean(errors.title)"
          @blur="touchField('title')"
        />
        <small v-if="errors.title" class="error-text">{{ errors.title }}</small>
      </div>

      <div class="field">
        <label for="property-address">Адрес</label>
        <InputText
          id="property-address"
          v-model="form.address"
          fluid
          :invalid="Boolean(errors.address)"
          @blur="touchField('address')"
        />
        <small v-if="errors.address" class="error-text">{{ errors.address }}</small>
      </div>

      <div class="field">
        <label for="property-type">Тип объекта</label>
        <Select
          id="property-type"
          v-model="form.property_type"
          :options="propertyTypeOptions"
          optionLabel="label"
          optionValue="value"
          fluid
          :invalid="Boolean(errors.property_type)"
          @blur="touchField('property_type')"
        />
        <small v-if="errors.property_type" class="error-text">{{ errors.property_type }}</small>
      </div>

      <div class="field field-description">
        <label for="property-description">Описание</label>
        <Textarea
          id="property-description"
          v-model="form.description"
          rows="4"
          fluid
          autoResize
          :invalid="Boolean(errors.description)"
          @blur="touchField('description')"
        />
        <small v-if="errors.description" class="error-text">{{ errors.description }}</small>
      </div>

      <div class="form-actions">
        <Button
          type="button"
          label="Отмена"
          severity="secondary"
          text
          size="small"
          :disabled="loading"
          @click="closeDialog"
        />
        <Button
          type="submit"
          :label="mode === 'edit' ? 'Сохранить' : 'Создать'"
          size="small"
          :loading="loading"
        />
      </div>
    </form>
  </Dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Select from 'primevue/select';
import Textarea from 'primevue/textarea';
import type { Property } from '../../shared/types';

type DialogMode = 'create' | 'edit';

type PropertyFormData = Pick<
  Property,
  'title' | 'address' | 'description' | 'property_type'
>;

type FormErrors = Partial<Record<keyof PropertyFormData, string>>;
type FormTouched = Partial<Record<keyof PropertyFormData, boolean>>;

interface Props {
  visible: boolean;
  mode?: DialogMode;
  loading?: boolean;
  initialValue?: Partial<PropertyFormData>;
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'create',
  loading: false,
  initialValue: () => ({}),
});

const emit = defineEmits<{
  'update:visible': [value: boolean];
  submit: [value: PropertyFormData];
}>();

const defaultFormData = (): PropertyFormData => ({
  title: '',
  address: '',
  description: '',
  property_type: 'apartment',
});

const form = reactive<PropertyFormData>(defaultFormData());
const errors = ref<FormErrors>({});
const touched = ref<FormTouched>({});

const propertyTypeOptions: Array<{ label: string; value: PropertyFormData['property_type'] }> = [
  { label: 'Квартира', value: 'apartment' },
  { label: 'Дом', value: 'house' },
  { label: 'Комната', value: 'room' },
  { label: 'Коммерция', value: 'commercial' },
];

const mode = computed(() => props.mode);
const visible = computed(() => props.visible);
const loading = computed(() => props.loading);

const resetForm = () => {
  const initial = props.initialValue;
  const nextForm = {
    ...defaultFormData(),
    ...initial,
  };

  form.title = nextForm.title;
  form.address = nextForm.address;
  form.description = nextForm.description;
  form.property_type = nextForm.property_type;
  errors.value = {};
  touched.value = {};
};

watch(
  () => props.visible,
  isOpen => {
    if (isOpen) {
      resetForm();
    }
  }
);

watch(
  () => props.initialValue,
  () => {
    if (props.visible) {
      resetForm();
    }
  },
  { deep: true }
);

const touchField = (field: keyof PropertyFormData) => {
  touched.value[field] = true;
};

const validate = (): boolean => {
  const nextErrors: FormErrors = {};

  // Базовые проверки. Здесь можно подключить zod/yup/vee-validate без изменения API компонента.
  if (!form.title.trim()) {
    nextErrors.title = 'Введите название объекта';
  }

  if (!form.address.trim()) {
    nextErrors.address = 'Введите адрес';
  }

  if (!form.property_type) {
    nextErrors.property_type = 'Выберите тип объекта';
  }

  if (!form.description.trim()) {
    nextErrors.description = 'Введите описание';
  }

  errors.value = nextErrors;
  return Object.keys(nextErrors).length === 0;
};

const closeDialog = () => {
  if (loading.value) return;
  emit('update:visible', false);
};

const handleDialogVisibility = (value: boolean) => {
  if (!value) {
    closeDialog();
    return;
  }

  emit('update:visible', true);
};

const handleSubmit = () => {
  touched.value = {
    title: true,
    address: true,
    description: true,
    property_type: true,
  };

  if (!validate()) {
    return;
  }

  emit('submit', {
    title: form.title.trim(),
    address: form.address.trim(),
    description: form.description.trim(),
    property_type: form.property_type,
  });
};
</script>

<style scoped>
.dialog-header h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: #111827;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.field label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
}

.field-description {
  margin-top: 0.1rem;
}

.error-text {
  color: #b91c1c;
  font-size: 0.75rem;
  line-height: 1.2;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.35rem;
  margin-top: 0.15rem;
}

:deep(.p-dialog .p-dialog-header) {
  padding: 0.9rem 1rem 0.6rem;
}

:deep(.p-dialog .p-dialog-content) {
  padding: 0 1rem 1rem;
}

:deep(.p-inputtext),
:deep(.p-select),
:deep(.p-textarea) {
  font-size: 0.9rem;
}
</style>
