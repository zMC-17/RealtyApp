<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Мои заявки</h1>
        <p>Создание обращения по обслуживанию или ремонту</p>
      </div>
    </div>

    <div v-if="isLoading" class="state state-loading">
      Загрузка формы...
    </div>

    <div v-else-if="errorMessage" class="state state-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="successMessage" class="state state-success">
      <h2>Заявка отправлена</h2>
      <p>{{ successMessage }}</p>
      <Button
        label="Создать ещё одну заявку"
        size="small"
        @click="resetForm"
      />
    </div>

    <Card v-else class="request-card">
      <template #content>
        <form class="request-form" @submit.prevent="handleSubmit">
          <div class="contract-info">
            <span class="contract-label">Договор</span>
            <strong>{{ currentContractReference }}</strong>
          </div>

          <div class="field">
            <label for="request-message">Сообщение</label>
            <Textarea
              id="request-message"
              v-model="message"
              rows="5"
              autoResize
              fluid
              placeholder="Кратко опишите проблему"
              :invalid="Boolean(fieldError)"
            />
            <small v-if="fieldError" class="error-text">{{ fieldError }}</small>
          </div>

          <div class="form-actions">
            <Button
              type="submit"
              label="Отправить заявку"
              size="small"
              :loading="isSubmitting"
            />
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Textarea from 'primevue/textarea';
import { createRequest } from '../../services/mock/requests';
import { getContractsByTenant } from '../../services/mock/contracts';
import { useAuthStore } from '../../stores/auth';

const authStore = useAuthStore();

const isLoading = ref(false);
const isSubmitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const message = ref('');
const currentContractId = ref('');
const currentContractReference = ref('');
const fieldError = ref('');

const getTenantId = (): string => authStore.user?.id ?? 'user_3';

const loadContract = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const contracts = await getContractsByTenant(getTenantId());

    if (contracts.length === 0) {
      currentContractId.value = '';
      currentContractReference.value = '';
      errorMessage.value = 'Для создания заявки нужен активный договор аренды.';
      return;
    }

    const contract = contracts[0];
    currentContractId.value = contract.id;
    currentContractReference.value = contract.id;
  } catch {
    errorMessage.value = 'Не удалось загрузить договор аренды. Попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

const resetForm = () => {
  message.value = '';
  fieldError.value = '';
  successMessage.value = '';
};

const handleSubmit = async () => {
  fieldError.value = '';
  errorMessage.value = '';
  successMessage.value = '';

  if (!message.value.trim()) {
    fieldError.value = 'Введите сообщение для заявки';
    return;
  }

  if (!currentContractId.value) {
    errorMessage.value = 'Невозможно создать заявку без активного договора.';
    return;
  }

  isSubmitting.value = true;

  try {
    await createRequest(currentContractId.value, message.value.trim());
    successMessage.value = 'Заявка принята. Владелец увидит её в списке обращений.';
    message.value = '';
  } catch {
    errorMessage.value = 'Не удалось отправить заявку. Попробуйте снова.';
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(loadContract);
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

.state-success h2 {
  margin: 0;
  font-size: 1.125rem;
  color: #111827;
}

.state-success p {
  margin: 0.45rem 0 0.9rem;
}

.state-error {
  border-color: #fecaca;
  background: #fef2f2;
  color: #991b1b;
}

.request-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}

.request-form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.contract-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.55rem 0.75rem;
  border-radius: 0.6rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
}

.contract-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #6b7280;
}

.contract-info strong {
  font-size: 0.95rem;
  color: #111827;
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
  margin-top: 0.05rem;
}

:deep(.request-card .p-card-body) {
  padding: 0.9rem 1rem;
}

:deep(.request-card .p-card-content) {
  padding: 0;
}

:deep(.p-inputtextarea) {
  font-size: 0.9rem;
}

@media (max-width: 900px) {
  .page-container {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
