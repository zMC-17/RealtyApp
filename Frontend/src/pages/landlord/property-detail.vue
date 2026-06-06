<!-- pages/landlord/property-detail.vue -->
<template>
    <div class="property-detail-page">
        <!-- Кнопка назад -->
        <button class="back-btn" @click="router.push({ name: 'LandlordProperties' })">
            ← Назад к объектам
        </button>

        <!-- Индикатор загрузки -->
        <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Загрузка...</p>
        </div>

        <!-- Контент -->
        <template v-else-if="property">
            <h1 class="property-title">{{ property.title }}</h1>

            <!-- Табы -->
            <div class="tabs">
                <button v-for="tab in visibleTabs" :key="tab.id" class="tab" :class="{ active: activeTab === tab.id }"
                    @click="activeTab = tab.id">
                    {{ tab.label }}
                </button>
            </div>

            <!-- Содержимое табов -->
            <div class="tab-content">
                <PropertyOverview v-if="activeTab === 'overview'" :property="property" @edit="openEditModal"
                    @delete="openDeleteModal" />

                <PropertyContract v-if="activeTab === 'contract'" :property-id="property.id" :contract="contract"
                    @contract-created="loadContract" />

                <PropertyPayments v-if="activeTab === 'payments' && contract" :contract-id="contract.id" />

                <PropertyRequests v-if="activeTab === 'requests' && contract" :contract-id="contract.id" />
            </div>
        </template>

        <!-- Модалки -->
        <EditPropertyModal v-if="showEditModal" :property="property" @close="showEditModal = false"
            @updated="onPropertyUpdated" />

        <DeletePropertyModal v-if="showDeleteModal" :property="property" @close="showDeleteModal = false"
            @deleted="onPropertyDeleted" />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePropertiesStore } from '../../stores/properties';
import type { ContractResponse } from '../../types/contract';
import { contractsService } from '../../services/contracts';
import PropertyOverview from '../../components/properties/PropertyOverview.vue';
import PropertyContract from '../../components/properties/PropertyContract.vue';
import PropertyPayments from '../../components/properties/PropertyPayments.vue';
import PropertyRequests from '../../components/properties/PropertyRequests.vue';
import EditPropertyModal from '../../components/properties/EditPropertyModal.vue';
import DeletePropertyModal from '../../components/properties/DeletePropertyModal.vue';

const route = useRoute();
const router = useRouter();
const propertiesStore = usePropertiesStore();

const loading = ref(true);
const property = ref(null);
const contract = ref<ContractResponse | null>(null);
const activeTab = ref('overview');
const showEditModal = ref(false);
const showDeleteModal = ref(false);

const visibleTabs = computed(() => {
    const tabs = [{ id: 'overview', label: 'Обзор' }];
    tabs.push({ id: 'contract', label: 'Договор' });

    if (contract.value) {
        tabs.push({ id: 'payments', label: 'Платежи' });
        tabs.push({ id: 'requests', label: 'Заявки' });
    }

    return tabs;
});

const loadProperty = async () => {
    const id = Number(route.params.id);
    property.value = await propertiesStore.fetchProperty(id);

    // Пытаемся загрузить договор
    try {
        const contracts = await contractsService.getOwnerContracts();
        contract.value = contracts.find(c => c.property_id === id) || null;
    } catch {
        contract.value = null;
    }

    loading.value = false;
};

const loadContract = async () => {
    const id = Number(route.params.id);
    try {
        const contracts = await contractsService.getOwnerContracts();
        contract.value = contracts.find(c => c.property_id === id) || null;
    } catch {
        contract.value = null;
    }
};

const openEditModal = () => { showEditModal.value = true; };
const openDeleteModal = () => { showDeleteModal.value = true; };

const onPropertyUpdated = (updated: any) => {
    property.value = updated;
    showEditModal.value = false;
};

const onPropertyDeleted = () => {
    router.push({ name: 'LandlordProperties' });
};

onMounted(loadProperty);
</script>

<style scoped>
.property-detail-page {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.back-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    color: #374151;
    cursor: pointer;
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
    transition: background 0.2s;
}

.back-btn:hover {
    background: #e5e7eb;
}

.property-title {
    font-size: 1.75rem;
    color: #1f2937;
    margin: 0 0 1.5rem 0;
}

.tabs {
    display: flex;
    gap: 0.25rem;
    border-bottom: 2px solid #e5e7eb;
    margin-bottom: 2rem;
}

.tab {
    padding: 0.75rem 1.5rem;
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    color: #6b7280;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s;
}

.tab:hover {
    color: #374151;
}

.tab.active {
    color: #667eea;
    border-bottom-color: #667eea;
}

.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e5e7eb;
    border-top: 4px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>