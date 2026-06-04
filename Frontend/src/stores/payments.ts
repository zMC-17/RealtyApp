// stores/payments.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { paymentsService } from '../services/payments.ts';
import type { PaymentResponse } from '../types/payment';

export const usePaymentsStore = defineStore('payments', () => {
    // ===== Состояние =====
    const payments = ref<PaymentResponse[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    // ===== Геттеры =====
    // Платежи, требующие подтверждения
    const waitingConfirmationPayments = computed(() =>
        payments.value.filter(p => p.status === 'waiting_confirmation')
    );

    // Просроченные платежи
    const overduePayments = computed(() =>
        payments.value.filter(p => p.status === 'overdue')
    );

    // Платежи, требующие внимания (подтверждение + просроченные)
    const attentionPayments = computed(() =>
        payments.value.filter(p =>
            p.status === 'waiting_confirmation' || p.status === 'overdue'
        )
    );

    // 5 ближайших платежей (по дате, исключая attention)
    const upcomingPayments = computed(() =>
        payments.value
            .filter(p => p.status !== 'waiting_confirmation' && p.status !== 'overdue')
            .sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime())
            .slice(0, 5)
    );

    // Есть ли платежи требующие внимания
    const hasAttentionPayments = computed(() => attentionPayments.value.length > 0);

    // ===== Действия =====
    /**
     * Загрузить все платежи владельца
     */
    async function fetchPayments() {
        loading.value = true;
        error.value = null;

        try {
            payments.value = await paymentsService.getOwnerPayments();
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка загрузки платежей';
            console.error('Ошибка загрузки платежей:', err);
        } finally {
            loading.value = false;
        }
    }

    /**
     * Подтвердить платёж
     */
    async function confirmPayment(paymentId: number) {
        loading.value = true;
        error.value = null;

        try {
            const updated = await paymentsService.confirmPayment(paymentId);
            // Обновляем платёж в массиве
            const index = payments.value.findIndex(p => p.id === paymentId);
            if (index !== -1) {
                payments.value[index] = updated;
            }
            return true;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка подтверждения платежа';
            console.error('Ошибка подтверждения платежа:', err);
            return false;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Отклонить подтверждение платежа
     */
    async function rejectPayment(paymentId: number) {
        loading.value = true;
        error.value = null;

        try {
            const updated = await paymentsService.rejectPayment(paymentId);
            // Обновляем платёж в массиве
            const index = payments.value.findIndex(p => p.id === paymentId);
            if (index !== -1) {
                payments.value[index] = updated;
            }
            return true;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка отклонения платежа';
            console.error('Ошибка отклонения платежа:', err);
            return false;
        } finally {
            loading.value = false;
        }
    }

    function clearError() {
        error.value = null;
    }

    return {
        payments,
        loading,
        error,
        waitingConfirmationPayments,
        overduePayments,
        attentionPayments,
        upcomingPayments,
        hasAttentionPayments,
        fetchPayments,
        confirmPayment,
        rejectPayment,
        clearError,
    };
});