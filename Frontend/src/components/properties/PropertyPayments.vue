<!-- components/properties/PropertyPayments.vue -->
<template>
    <div class="property-payments">
        <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Загрузка платежей...</p>
        </div>

        <div v-else-if="payments.length === 0" class="empty-state">
            <div class="empty-icon">💰</div>
            <h3>Платежей пока нет</h3>
            <p>Платежи появятся после активации договора</p>
        </div>

        <div v-else class="payments-list">
            <PaymentCard v-for="payment in payments" :key="payment.id" :payment="payment" @confirm="handleConfirm"
                @reject="handleReject" />
        </div>

        <ConfirmPaymentModal v-if="showConfirmModal && selectedPayment" :visible="showConfirmModal"
            :payment="selectedPayment" @close="showConfirmModal = false" @confirmed="loadPayments" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { paymentsService } from '../../services/payments';
import { usePaymentsStore } from '../../stores/payments';
import type { PaymentResponse } from '../../types/payment';
import PaymentCard from '../payments/PaymentCard.vue';
import ConfirmPaymentModal from '../payments/ConfirmPaymentModal.vue';

const props = defineProps<{
    contractId: number;
}>();

const paymentsStore = usePaymentsStore();
const payments = ref<PaymentResponse[]>([]);
const loading = ref(true);
const showConfirmModal = ref(false);
const selectedPayment = ref<PaymentResponse | null>(null);

const loadPayments = async () => {
    loading.value = true;
    try {
        payments.value = await paymentsService.getContractPayments(props.contractId);
    } catch (error) {
        console.error('Ошибка загрузки платежей:', error);
    } finally {
        loading.value = false;
    }
};

const handleConfirm = (paymentId: number) => {
    const payment = payments.value.find(p => p.id === paymentId);
    if (payment) {
        selectedPayment.value = payment;
        showConfirmModal.value = true;
    }
};

const handleReject = async (paymentId: number) => {
    await paymentsStore.rejectPayment(paymentId);
    await loadPayments();
};

onMounted(loadPayments);
</script>

<style scoped>
.property-payments {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.payments-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.loading-state,
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 2rem;
    text-align: center;
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

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.empty-state h3 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
}

.empty-state p {
    color: #6b7280;
    margin: 0;
}
</style>÷