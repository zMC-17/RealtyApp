/**
 * Pinia хранилище для управления платежами
 *
 * Управляет состоянием платежей:
 * - Кэширование данных из mock сервиса
 * - Loading/error состояния
 * - Фильтрация платежей по статусам
 * - Операции с платежами (отметить как оплачено, создать и т.д.)
 *
 * Готово для замены на реальный API
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {
  getPaymentsByContract,
  getPaymentStats,
  markPaymentAsPaid,
  createPayment,
  deletePayment,
} from '../services/mock/payments';
import type { Payment, PaymentStatus } from '../shared/types';

export const usePaymentsStore = defineStore('payments', () => {
  // State
  const payments = ref<Payment[]>([]);
  const stats = ref({
    total_paid: 0,
    total_unpaid: 0,
    total_overdue: 0,
    overdue_count: 0,
  });
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const paidPayments = computed(() => payments.value.filter(p => p.status === 'paid'));
  const unpaidPayments = computed(() => payments.value.filter(p => p.status === 'unpaid'));
  const overduePayments = computed(() => payments.value.filter(p => p.status === 'overdue'));

  const filteredByStatus = (status: PaymentStatus) =>
    computed(() => payments.value.filter(p => p.status === status));

  // ============================================================
  // Actions
  // ============================================================

  /**
   * Загрузить платежи по договору
   */
  const fetchPaymentsByContract = async (contractId: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const data = await getPaymentsByContract(contractId);
      payments.value = data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки платежей';
      payments.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Загрузить статистику платежей по владельцу
   */
  const fetchPaymentStats = async (ownerId: string) => {
    try {
      const data = await getPaymentStats(ownerId);
      stats.value = data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки статистики';
    }
  };

  /**
   * Отметить платёж как оплаченный
   */
  const markAsPaid = async (paymentId: string) => {
    try {
      const updated = await markPaymentAsPaid(paymentId);
      const index = payments.value.findIndex(p => p.id === paymentId);
      if (index >= 0) {
        payments.value[index] = updated;
      }
      return updated;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка при обновлении платежа';
      throw err;
    }
  };

  /**
   * Создать новый платёж
   */
  const addPayment = async (contractId: string, amount: number, dueDate: string) => {
    try {
      const newPayment = await createPayment(contractId, dueDate, amount);
      payments.value.push(newPayment);
      return newPayment;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка создания платежа';
      throw err;
    }
  };

  /**
   * Удалить платёж
   */
  const removePayment = async (paymentId: string) => {
    try {
      await deletePayment(paymentId);
      payments.value = payments.value.filter(p => p.id !== paymentId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка удаления платежа';
      throw err;
    }
  };

  /**
   * Очистить состояние
   */
  const reset = () => {
    payments.value = [];
    stats.value = {
      total_paid: 0,
      total_unpaid: 0,
      total_overdue: 0,
      overdue_count: 0,
    };
    error.value = null;
    isLoading.value = false;
  };

  return {
    // State
    payments,
    stats,
    isLoading,
    error,

    // Computed
    paidPayments,
    unpaidPayments,
    overduePayments,
    filteredByStatus,

    // Actions
    fetchPaymentsByContract,
    fetchPaymentStats,
    markAsPaid,
    addPayment,
    removePayment,
    reset,
  };
});
