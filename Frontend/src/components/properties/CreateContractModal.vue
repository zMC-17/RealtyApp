<!-- components/properties/CreateContractModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Создание договора аренды</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-group">
          <label>Email арендатора *</label>
          <input v-model="form.tenant_email" type="email" required placeholder="tenant@example.com" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Дата начала *</label>
            <input type="date" v-model="form.start_date" required />
          </div>
          <div class="form-group">
            <label>Дата окончания *</label>
            <input type="date" v-model="form.end_date" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Ежемесячный платёж (₽) *</label>
            <input v-model.number="form.monthly_payment" type="number" required min="0" step="0.01"
              placeholder="50000" />
          </div>
          <div class="form-group">
            <label>Депозит (₽)</label>
            <input v-model.number="form.security_deposit" type="number" min="0" step="0.01"
              placeholder="50000" />
          </div>
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="$emit('close')">Отмена</button>
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Создание...' : 'Создать договор' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { contractsService } from '../../services/contracts';

const props = defineProps<{ propertyId: number }>();
const emit = defineEmits(['close', 'created']);

const loading = ref(false);
const error = ref('');

const form = reactive({
  tenant_email: '',
  start_date: '',
  end_date: '',
  monthly_payment: 0,
  security_deposit: 0,
});

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';

  try {
    await contractsService.createByEmail({
      property_id: props.propertyId,
      ...form,
    });
    emit('created');
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка создания договора';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #1f2937;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-cancel,
.btn-submit {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  color: #374151;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>