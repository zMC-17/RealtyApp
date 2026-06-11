<!-- components/properties/PropertyPayments.vue -->
<template>
    <div class="property-payments">

        <div v-if="loading" class="loader-wrap">
            <div class="loader-line"></div>
            <p class="loader-label">Загрузка платежей…</p>
        </div>

        <div v-else-if="payments.length === 0" class="empty-state">
            <div class="empty-icon-box">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <rect x="2" y="5" width="16" height="12" rx="2" stroke="currentColor" stroke-width="1.4" />
                    <path d="M2 9h16" stroke="currentColor" stroke-width="1.4" />
                    <circle cx="5.5" cy="13" r="1" fill="currentColor" />
                </svg>
            </div>
            <p class="empty-title">Платежей пока нет</p>
            <p class="empty-text">Платежи появятся после активации договора</p>
        </div>

        <template v-else>
            <!-- Шапка колонок -->
            <div class="list-header">
                <div>Статус</div>
                <div>Дата</div>
                <div style="text-align:right">Сумма</div>
                <div></div>
            </div>

            <div class="payments-list">
                <PaymentCard v-for="payment in payments" :key="payment.id" :payment="payment" @confirm="handleConfirm"
                    @reject="handleReject" />
            </div>
        </template>

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

const props = defineProps<{ contractId: number }>();

const paymentsStore = usePaymentsStore();
const payments = ref<PaymentResponse[]>([]);
const loading = ref(true);
const showConfirmModal = ref(false);
const selectedPayment = ref<PaymentResponse | null>(null);

const loadPayments = async () => {
    loading.value = true;
    try { payments.value = await paymentsService.getContractPayments(props.contractId); }
    catch (err) { console.error(err); }
    finally { loading.value = false; }
};

const handleConfirm = (paymentId: number) => {
    selectedPayment.value = payments.value.find(p => p.id === paymentId) || null;
    showConfirmModal.value = true;
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
    gap: var(--space-3);
}

.loader-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-12);
}

.loader-line {
    width: 120px;
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

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-12) var(--space-8);
    text-align: center;
}

.empty-icon-box {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-lg);
    background: rgba(255, 255, 255, 0.52);
    border: 1px solid rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--space-2);
    color: var(--color-dark-35);
}

.empty-title {
    font-size: var(--text-md);
    font-weight: 700;
    color: var(--color-dark);
    letter-spacing: -0.02em;
}

.empty-text {
    font-size: var(--text-sm);
    color: var(--color-dark-35);
}

/* Шапка колонок — выровнена под PaymentCard (3px + gap + 160px + ...) */
.list-header {
    display: grid;
    grid-template-columns: 160px 1fr auto 72px;
    gap: var(--space-4);
    padding: 0 var(--space-5) var(--space-1) calc(3px + var(--space-4));
}

.list-header>div {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--color-dark-35);
}

.payments-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}
</style>