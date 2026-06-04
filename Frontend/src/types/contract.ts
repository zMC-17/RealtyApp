// types/contract.ts

export interface ContractCreateByEmail {
    property_id: number;
    tenant_email: string;
    start_date: string;
    end_date: string;
    monthly_payment: number;
    security_deposit?: number;
}

export const CONTRACT_STATUS_LABELS: Record<string, string> = {
    'pending_tenant_confirmation': 'Ожидает подтверждения арендатором',
    'active': 'Активен',
    'completed': 'Завершён',
    'cancelled': 'Отменён',
};

// types/contract.ts — обновите

export interface OwnerInfo {
    id: number;
    name: string;
    email: string;
}

export interface PropertyInfo {
    id: number;
    title: string;
    address: string;
}

export interface ContractResponse {
    id: number;
    property_id: number;
    tenant_id: number;
    start_date: string;
    end_date: string;
    monthly_payment: string;
    security_deposit: string;
    status: string;
}

export interface ContractWithDetails extends ContractResponse {
    property_info?: PropertyInfo;
    owner_info?: OwnerInfo;
}