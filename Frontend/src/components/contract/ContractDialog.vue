<template>
  <Dialog
    :visible="visible"
    :modal="true"
    :draggable="false"
    :closable="!loading"
    :style="{ width: '36rem' }"
    :content-style="{ backgroundColor: 'white' }"
    :breakpoints="{ '960px': '94vw' }"
    @update:visible="handleDialogVisibility"
  >
    <template #header>
      <div class="dialog-header">
        <h3>Новый договор аренды</h3>
      </div>
    </template>

    <form class="form-grid" @submit.prevent="handleSubmit">
      <div class="field">
        <label for="contract-property">Объект недвижимости</label>
        <Dropdown
          id="contract-property"
          v-model="form.property_id"
          :options="propertyOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Выберите объект"
          fluid
          :invalid="Boolean(errors.property_id)"
          @blur="touchField('property_id')"
        />
        <small v-if="errors.property_id" class="error-text">{{ errors.property_id }}</small>
      </div>

      <div class="field">
        <label for="contract-tenant">Арендатор (username)</label>
        <Dropdown
          id="contract-tenant"
          v-model="form.tenant_id"
          :options="tenantOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Выберите арендатора"
          filter
          fluid
          :invalid="Boolean(errors.tenant_id)"
          @blur="touchField('tenant_id')"
        />
        <small v-if="errors.tenant_id" class="error-text">{{ errors.tenant_id }}</small>
      </div>

      <div class="field-grid-2">
        <div class="field">
          <label for="contract-start">Дата начала</label>
          <Calendar
            id="contract-start"
            v-model="form.start_date"
            dateFormat="dd.mm.yy"
            showIcon
            fluid
            :invalid="Boolean(errors.start_date)"
            @blur="touchField('start_date')"
          />
          <small v-if="errors.start_date" class="error-text">{{ errors.start_date }}</small>
        </div>

        <div class="field">
          <label for="contract-end">Дата окончания</label>
          <Calendar
            id="contract-end"
            v-model="form.end_date"
            dateFormat="dd.mm.yy"
            showIcon
            fluid
            :invalid="Boolean(errors.end_date)"
            @blur="touchField('end_date')"
          />
          <small v-if="errors.end_date" class="error-text">{{ errors.end_date }}</small>
        </div>
      </div>

      <div class="field">
        <label for="contract-payment">Ежемесячный платёж</label>
        <InputNumber
          id="contract-payment"
          v-model="form.monthly_payment"
          mode="currency"
          currency="RUB"
          locale="ru-RU"
          :min="0"
          fluid
          :invalid="Boolean(errors.monthly_payment)"
          @blur="touchField('monthly_payment')"
        />
        <small v-if="errors.monthly_payment" class="error-text">{{ errors.monthly_payment }}</small>
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
          label="Создать договор"
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
import Calendar from 'primevue/datepicker';
import Dropdown from 'primevue/select';
import InputNumber from 'primevue/inputnumber';

interface SelectOption {
  label: string;
  value: string;
}

interface ContractDialogSubmit {
  property_id: string;
  tenant_id: string;
  start_date: string;
  end_date: string;
  monthly_payment: number;
}

interface FormState {
  property_id: string;
  tenant_id: string;
  start_date: Date | null;
  end_date: Date | null;
  monthly_payment: number | null;
}

type FormErrors = Partial<Record<keyof FormState, string>>;

type FormTouched = Partial<Record<keyof FormState, boolean>>;

interface Props {
  visible: boolean;
  loading?: boolean;
  propertyOptions: SelectOption[];
  tenantOptions: SelectOption[];
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
});

const emit = defineEmits<{
  'update:visible': [value: boolean];
  submit: [value: ContractDialogSubmit];
}>();

const visible = computed(() => props.visible);
const loading = computed(() => props.loading);
const propertyOptions = computed(() => props.propertyOptions);
const tenantOptions = computed(() => props.tenantOptions);

const defaultFormState = (): FormState => ({
  property_id: '',
  tenant_id: '',
  start_date: null,
  end_date: null,
  monthly_payment: null,
});

const form = reactive<FormState>(defaultFormState());
const errors = ref<FormErrors>({});
const touched = ref<FormTouched>({});

const resetForm = () => {
  const next = defaultFormState();
  form.property_id = next.property_id;
  form.tenant_id = next.tenant_id;
  form.start_date = next.start_date;
  form.end_date = next.end_date;
  form.monthly_payment = next.monthly_payment;
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

const touchField = (field: keyof FormState) => {
  touched.value[field] = true;
};

const toApiDate = (value: Date | null): string => {
  if (!value) return '';
  return value.toISOString().slice(0, 10);
};

const validate = (): boolean => {
  const nextErrors: FormErrors = {};

  if (!form.property_id) {
    nextErrors.property_id = 'Выберите объект недвижимости';
  }

  if (!form.tenant_id) {
    nextErrors.tenant_id = 'Выберите арендатора';
  }

  if (!form.start_date) {
    nextErrors.start_date = 'Укажите дату начала';
  }

  if (!form.end_date) {
    nextErrors.end_date = 'Укажите дату окончания';
  }

  if (form.start_date && form.end_date && form.end_date < form.start_date) {
    nextErrors.end_date = 'Дата окончания не может быть раньше даты начала';
  }

  if (form.monthly_payment === null || form.monthly_payment <= 0) {
    nextErrors.monthly_payment = 'Введите сумму ежемесячного платежа';
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
    property_id: true,
    tenant_id: true,
    start_date: true,
    end_date: true,
    monthly_payment: true,
  };

  if (!validate()) {
    return;
  }

  emit('submit', {
    property_id: form.property_id,
    tenant_id: form.tenant_id,
    start_date: toApiDate(form.start_date),
    end_date: toApiDate(form.end_date),
    monthly_payment: form.monthly_payment ?? 0,
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
  gap: 0.7rem;
  margin-top: 0.2rem;
}

.field-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.65rem;
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
  margin-top: 0.1rem;
}

:deep(.p-dialog .p-dialog-header) {
  padding: 0.9rem 1rem 0.6rem;
}

:deep(.p-dialog .p-dialog-content) {
  padding: 0 1rem 1rem;
}

:deep(.p-inputtext),
:deep(.p-select),
:deep(.p-datepicker-input),
:deep(.p-inputnumber-input) {
  font-size: 0.9rem;
}

@media (max-width: 900px) {
  .field-grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
