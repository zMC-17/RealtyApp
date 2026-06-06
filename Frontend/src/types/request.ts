// types/request.ts

export type RequestStatus = 'open' | 'in_progress' | 'completed' | 'cancelled';

export const REQUEST_STATUS_LABELS: Record<RequestStatus, string> = {
    open: 'Открыта',
    in_progress: 'В работе',
    completed: 'Выполнена',
    cancelled: 'Отменена',
};

export const REQUEST_STATUS_COLORS: Record<RequestStatus, string> = {
    open: '#ef4444',
    in_progress: '#f59e0b',
    completed: '#10b981',
    cancelled: '#6b7280',
};

export interface RequestResponse {
    id: number;
    contract_id: number;
    title: string;
    message: string;
    status: RequestStatus;
    created_at?: string;
}

export interface RequestWithDetails extends RequestResponse {
    contract_info?: {
        id: number;
        start_date: string;
        end_date: string;
        monthly_payment: string;
    };
    property_info?: {
        id: number;
        title: string;
        address: string;
    };
    tenant_info?: {
        id: number;
        name: string;
        email: string;
    };
    owner_info?: {
        id: number;
        name: string;
        email: string;
    };
}

export interface RequestCreate {
    contract_id: number;
    title: string;
    message: string;
}