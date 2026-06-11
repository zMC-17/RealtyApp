<!-- pages/landlord/property-detail.vue -->
<template>
    <div class="content-page">
        <div class="content-inner">

            <!-- Кнопка назад -->
            <button class="back-btn" @click="router.push({ name: 'LandlordProperties' })">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M9 2L3 7l6 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
                        stroke-linejoin="round" />
                </svg>
                Назад к объектам
            </button>

            <!-- Лоадер -->
            <div v-if="loading" class="loader-wrap">
                <div class="loader-line"></div>
                <p class="loader-label">Загрузка…</p>
            </div>

            <template v-else-if="property">

                <h1 class="page-title">{{ property.title }}</h1>

                <!-- Табы -->
                <div class="tabs">
                    <button v-for="tab in visibleTabs" :key="tab.id" class="tab"
                        :class="{ active: activeTab === tab.id }" @click="activeTab = tab.id">
                        {{ tab.label }}
                    </button>
                </div>

                <!-- Содержимое -->
                <div class="tab-content">
                    <PropertyOverview v-if="activeTab === 'overview'" :property="property" @edit="openEditModal"
                        @delete="openDeleteModal" />
                    <PropertyContract v-if="activeTab === 'contract'" :property-id="property.id" :contract="contract"
                        @contract-created="loadContract" />
                    <PropertyPayments v-if="activeTab === 'payments' && contract" :contract-id="contract.id" />
                    <PropertyRequests v-if="activeTab === 'requests' && contract" :contract-id="contract.id" />
                </div>

            </template>

        </div>
    </div>

    <EditPropertyModal v-if="showEditModal" :property="property" @close="showEditModal = false"
        @updated="onPropertyUpdated" />
    <DeletePropertyModal v-if="showDeleteModal" :property="property" @close="showDeleteModal = false"
        @deleted="onPropertyDeleted" />
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
const property = ref<any>(null);
const contract = ref<ContractResponse | null>(null);
const activeTab = ref('overview');
const showEditModal = ref(false);
const showDeleteModal = ref(false);

const visibleTabs = computed(() => {
    const tabs = [
        { id: 'overview', label: 'Обзор' },
        { id: 'contract', label: 'Договор' },
    ];
    if (contract.value) {
        tabs.push({ id: 'payments', label: 'Платежи' });
        tabs.push({ id: 'requests', label: 'Заявки' });
    }
    return tabs;
});

const loadProperty = async () => {
    const id = Number(route.params.id);
    property.value = await propertiesStore.fetchProperty(id);
    try {
        const contracts = await contractsService.getOwnerContracts();
        contract.value = contracts.find(c => c.property_id === id) || null;
    } catch { contract.value = null; }
    loading.value = false;
};

const loadContract = async () => {
    const id = Number(route.params.id);
    try {
        const contracts = await contractsService.getOwnerContracts();
        contract.value = contracts.find(c => c.property_id === id) || null;
    } catch { contract.value = null; }
};

const openEditModal = () => { showEditModal.value = true; };
const openDeleteModal = () => { showDeleteModal.value = true; };
const onPropertyUpdated = (updated: any) => { property.value = updated; showEditModal.value = false; };
const onPropertyDeleted = () => router.push({ name: 'LandlordProperties' });

onMounted(loadProperty);
</script>

<style scoped>
.back-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    background: rgba(255, 255, 255, 0.50);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: var(--radius-md);
    color: var(--color-dark-60);
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition);
    margin-bottom: var(--space-6);
}

.back-btn:hover {
    background: rgba(255, 255, 255, 0.70);
    color: var(--color-dark);
}

/* ---- Лоадер ---- */
.loader-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-16);
}

.loader-line {
    width: 160px;
    height: 2px;
    background: rgba(28, 26, 23, 0.10);
    border-radius: 1px;
    overflow: hidden;
    position: relative;
}

.loader-line::after {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--color-emerald);
    animation: loader 1.4s ease-in-out infinite;
}

@keyframes loader {
    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(200%);
    }
}

.loader-label {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
}

/* ---- Заголовок ---- */
.page-title {
    font-size: var(--text-3xl);
    font-weight: 800;
    color: var(--color-dark);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: var(--space-6);
}

/* ---- Табы ---- */
.tabs {
    display: flex;
    gap: 2px;
    border-bottom: 1px solid rgba(28, 26, 23, 0.10);
    margin-bottom: var(--space-8);
}

.tab {
    padding: var(--space-3) var(--space-5);
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    color: var(--color-dark-60);
    font-family: var(--font-base);
    font-size: var(--text-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition);
    white-space: nowrap;
}

.tab:hover {
    color: var(--color-dark);
}

.tab.active {
    color: var(--color-emerald);
    border-bottom-color: var(--color-emerald);
    font-weight: 600;
}
</style>