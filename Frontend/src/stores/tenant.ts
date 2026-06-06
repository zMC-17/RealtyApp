// stores/tenant.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { contractsService } from '../services/contracts';
import type { ContractWithDetails } from '../types/contract';

export const useTenantStore = defineStore('tenant', () => {
    const contracts = ref<ContractWithDetails[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    // Активный договор (со статусом active)
    const activeContract = computed(() =>
        contracts.value.find(c => c.status === 'active') || null
    );

    // Договоры, ожидающие подтверждения
    const pendingContracts = computed(() =>
        contracts.value.filter(c => c.status === 'pending_tenant_confirmation')
    );

    // Есть ли активный договор
    const hasActiveContract = computed(() => !!activeContract.value);

    // Есть ли ожидающие договоры
    const hasPendingContracts = computed(() => pendingContracts.value.length > 0);

    async function fetchContracts() {
        loading.value = true;
        error.value = null;
        try {
            contracts.value = await contractsService.getTenantContracts();
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка загрузки договоров';
        } finally {
            loading.value = false;
        }
    }

    async function confirmContract(contractId: number) {
        loading.value = true;
        error.value = null;
        try {
            await contractsService.confirmContract(contractId);
            await fetchContracts(); // обновляем список
            return true;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка подтверждения договора';
            return false;
        } finally {
            loading.value = false;
        }
    }

    return {
        contracts,
        loading,
        error,
        activeContract,
        pendingContracts,
        hasActiveContract,
        hasPendingContracts,
        fetchContracts,
        confirmContract,
    };
});