import apiClient from './client';

export async function getPaymentsByContract(contractId: number): Promise<unknown[]> {
  return apiClient.get<unknown[]>(`/payments/contracts/${contractId}`);
}

export async function getPaymentById(paymentId: number): Promise<unknown> {
  return apiClient.get<unknown>(`/payments/${paymentId}`);
}

export async function getOverduePayments(): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/payments/owner/me');
}

export async function getPaymentStats(): Promise<unknown> {
  return apiClient.get<unknown>('/payments/owner/me');
}

export async function createPayment(data: unknown): Promise<unknown> {
  return apiClient.post<unknown>('/payments', data);
}

export async function markPaymentAsPaid(paymentId: number, paidAt: string = new Date().toISOString()): Promise<unknown> {
  return apiClient.put<unknown>(`/payments/${paymentId}`, { paid_at: paidAt, status: 'paid' });
}

export async function updatePayment(paymentId: number, data: unknown): Promise<unknown> {
  return apiClient.put<unknown>(`/payments/${paymentId}`, data);
}

export async function deletePayment(paymentId: number): Promise<boolean> {
  await apiClient.delete(`/payments/${paymentId}`);
  return true;
}

export default { getPaymentsByContract, getPaymentById, getOverduePayments, getPaymentStats, createPayment, markPaymentAsPaid, updatePayment, deletePayment };
