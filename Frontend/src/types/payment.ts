// types/payment.ts

export type PaymentStatus = 'pending' | 'waiting_confirmation' | 'overdue' | 'paid';

export interface ContractInfo {
    id: number;
    start_date: string;
    end_date: string;
    monthly_payment: string;
}

export interface PropertyInfo {
    id: number;
    title: string;
    address: string;
}

export interface TenantInfo {
    id: number;
    name: string;
    email: string;
}

export interface PaymentResponse {
    id: number;
    contract_id: number;
    amount: string;
    due_date: string;
    paid_at: string | null;
    status: PaymentStatus;
    comment: string | null;
    payment_proof_url: string | null;
    confirmation_requested_at: string | null;
    // Расширенные поля
    contract_info?: ContractInfo;
    property_info?: PropertyInfo;
    tenant_info?: TenantInfo;
}

// Константы для статусов
export const PAYMENT_STATUS_LABELS: Record<PaymentStatus, string> = {
    pending: 'Ожидает оплаты',
    waiting_confirmation: 'Требует подтверждения',
    overdue: 'Просрочен',
    paid: 'Оплачен',
};

export const PAYMENT_STATUS_COLORS: Record<PaymentStatus, string> = {
    pending: '#f59e0b',           // янтарный
    waiting_confirmation: '#3b82f6', // синий
    overdue: '#ef4444',           // красный
    paid: '#10b981',              // зелёный
};