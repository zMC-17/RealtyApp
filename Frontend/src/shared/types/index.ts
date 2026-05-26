// ============================================================
// ПЕРЕЧИСЛЕНИЯ СТАТУСОВ (Enums)
// ============================================================

export type UserRole = 'landlord' | 'tenant';

export type ContractStatus = 'pending' | 'active' | 'terminated';

export type PaymentStatus = 'unpaid' | 'overdue' | 'paid';

export type RequestStatus = 'new' | 'in_progress' | 'completed';

// ============================================================
// ОСНОВНЫЕ СУЩНОСТИ (Entities)
// ============================================================

export interface User {
  id: string;
  email: string;
  username: string;
  password_hash: string;
  created_at: string;
}

export interface Property {
  id: string;
  owner_id: string;
  title: string;
  address: string;
  description: string;
  property_type: 'apartment' | 'house' | 'room' | 'commercial';
  created_at: string;
}


export interface Contract {
  id: string;
  property_id: string;
  tenant_id: string;
  start_date: string;
  end_date: string;
  monthly_payment: number;
  status: ContractStatus;
  created_at: string;
}


export interface Payment {
  id: string;
  contract_id: string;
  amount: number;
  due_date: string;
  paid_at: string | null;
  status: PaymentStatus;
  comment: string;
  created_at: string;
}

export interface Request {
  id: string;
  contract_id: string;
  message: string;
  status: RequestStatus;
  created_at: string;
}

export interface LandlordStatistics {
  total_income: number;
  properties_count: number;
  active_contracts_count: number;
  overdue_payments_count: number;
}

// ============================================================
// ТИПЫ ДЛЯ АУТЕНТИФИКАЦИИ
// ============================================================

export interface AuthSession {
  user: User;
  access_token: string;
  current_role: UserRole;
}

// ============================================================
// КОНСТАНТЫ ДЛЯ UI (Dropdowns, Filters, Validations)
// ============================================================

export const CONTRACT_STATUS_VALUES = ['pending', 'active', 'terminated'] as const;

export const PAYMENT_STATUS_VALUES = ['unpaid', 'overdue', 'paid'] as const;

export const REQUEST_STATUS_VALUES = ['new', 'in_progress', 'completed'] as const;

/**
 * Метки для отображения статусов в UI
 *
 * ДИЗАЙН: Удобные текстовые представления статусов для пользователей.
 * Используются в таблицах, фильтрах, уведомлениях.
 */

export const CONTRACT_STATUS_LABELS: Record<ContractStatus, string> = {
  pending: 'Ожидание подписания',
  active: 'Активен',
  terminated: 'Расторгнут',
};

export const PAYMENT_STATUS_LABELS: Record<PaymentStatus, string> = {
  unpaid: 'Не оплачен',
  overdue: 'Просрочен',
  paid: 'Оплачен',
};

export const REQUEST_STATUS_LABELS: Record<RequestStatus, string> = {
  new: 'Новая',
  in_progress: 'В работе',
  completed: 'Выполнена',
};

export const CONTRACT_STATUS_COLORS: Record<ContractStatus, string> = {
  pending: '#9ca3af',
  active: '#3b82f6',
  terminated: '#6b7280',
};

export const PAYMENT_STATUS_COLORS: Record<PaymentStatus, string> = {
  unpaid: '#9ca3af',
  overdue: '#ef4444',
  paid: '#10b981',
};

export const REQUEST_STATUS_COLORS: Record<RequestStatus, string> = {
  new: '#9ca3af',
  in_progress: '#3b82f6',
  completed: '#10b981',
};
