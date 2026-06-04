// services/payments.service.ts
import api from './api';
import type { PaymentResponse } from '../types/payment';

export const paymentsService = {
    /**
     * Получить все платежи владельца (с расширенной информацией)
     */
    async getOwnerPayments(): Promise<PaymentResponse[]> {
        const { data } = await api.get<PaymentResponse[]>('/payments/owner/me');
        return data;
    },

    /**
     * Подтвердить платёж
     */
    async confirmPayment(paymentId: number): Promise<PaymentResponse> {
        const { data } = await api.post<PaymentResponse>(`/payments/${paymentId}/confirm`);
        return data;
    },

    /**
     * Отклонить подтверждение платежа
     */
    async rejectPayment(paymentId: number): Promise<PaymentResponse> {
        const { data } = await api.post<PaymentResponse>(`/payments/${paymentId}/reject`);
        return data;
    },

    /**
   * Получить платежи по конкретному договору
   */
    async getContractPayments(contractId: number): Promise<PaymentResponse[]> {
        const { data } = await api.get<PaymentResponse[]>(`/payments/contracts/${contractId}`);
        return data;
    },

    // services/payments.service.ts — добавьте

    async getTenantPayments(): Promise<PaymentResponse[]> {
        const { data } = await api.get<PaymentResponse[]>('/payments/tenant/me');
        return data;
    },

    async requestConfirmation(
        paymentId: number,
        payload: {
            payment_proof_url: string;  // теперь это просто текст (ссылка или что угодно)
            comment?: string;
        }
    ): Promise<PaymentResponse> {
        const { data } = await api.post<PaymentResponse>(
            `/payments/${paymentId}/request-confirmation`,
            payload
        );
        return data;
    },
};