<!-- components/properties/PropertyContract.vue -->
<template>
    <div class="property-contract">
        <!-- Договор существует -->
        <template v-if="contract">
            <div class="contract-card">
                <h3>Договор аренды #{{ contract.id }}</h3>

                <div class="contract-info">
                    <div class="info-row">
                        <span>Статус:</span>
                        <span class="status-badge" :class="statusClass">
                            {{ statusLabel }}
                        </span>
                    </div>
                    <div class="info-row">
                        <span>Период:</span>
                        <span>{{ formatDate(contract.start_date) }} — {{ formatDate(contract.end_date) }}</span>
                    </div>
                    <div class="info-row">
                        <span>Ежемесячный платёж:</span>
                        <span class="amount">{{ formatCurrency(contract.monthly_payment) }}</span>
                    </div>
                    <div class="info-row">
                        <span>Депозит:</span>
                        <span>{{ formatCurrency(contract.security_deposit) }}</span>
                    </div>
                </div>
            </div>
        </template>

        <!-- Нет договора — форма создания -->
        <template v-else>
            <div class="no-contract">
                <div class="no-contract-icon">📋</div>
                <h3>Договор аренды отсутствует</h3>
                <p>Создайте договор, указав email арендатора и условия аренды</p>
                <button class="btn-create" @click="showCreateModal = true">
                    + Создать договор
                </button>
            </div>

            <CreateContractModal v-if="showCreateModal" :property-id="propertyId" @close="showCreateModal = false"
                @created="onContractCreated" />
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { ContractResponse } from '../../types/contract';
import { CONTRACT_STATUS_LABELS } from '../../types/contract';
import CreateContractModal from './CreateContractModal.vue';

const props = defineProps<{
    propertyId: number;
    contract: ContractResponse | null;
}>();

const emit = defineEmits(['contract-created']);
const showCreateModal = ref(false);

const statusLabel = computed(() => CONTRACT_STATUS_LABELS[props.contract?.status || '']);
const statusClass = computed(() => props.contract?.status || '');

const onContractCreated = () => {
    showCreateModal.value = false;
    emit('contract-created');
};

const formatDate = (date: string) => new Date(date).toLocaleDateString('ru-RU');
const formatCurrency = (value: string) =>
    new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(parseFloat(value));
</script>

<style scoped>
/* Стили для контракта и формы */
.contract-card,
.no-contract {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.no-contract {
    text-align: center;
}

.no-contract-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.btn-create {
    margin-top: 1.5rem;
    padding: 0.75rem 2rem;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
}
</style>