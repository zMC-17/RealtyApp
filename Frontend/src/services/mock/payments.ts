/**
 * Mock сервис для управления платежами
 *
 * Симулирует API запросы к /api/payments
 */

import type { Payment } from '../../shared/types';

// ============================================================
// MOCK ДАННЫЕ
// ============================================================

const MOCK_PAYMENTS: Payment[] = [
  {
    id: 'payment_1',
    contract_id: 'contract_1',
    amount: 50000,
    due_date: '2024-01-31',
    paid_at: '2024-01-28T15:30:00Z',
    status: 'paid',
    comment: 'Оплачено вовремя',
    created_at: '2024-01-01T10:00:00Z',
  },
  {
    id: 'payment_2',
    contract_id: 'contract_1',
    amount: 50000,
    due_date: '2024-02-29',
    paid_at: null,
    status: 'overdue',
    comment: 'Требуется внимание',
    created_at: '2024-02-01T10:00:00Z',
  },
  {
    id: 'payment_3',
    contract_id: 'contract_1',
    amount: 50000,
    due_date: '2024-03-31',
    paid_at: null,
    status: 'unpaid',
    comment: 'Ждём платежа',
    created_at: '2024-03-01T10:00:00Z',
  },
  {
    id: 'payment_4',
    contract_id: 'contract_2',
    amount: 150000,
    due_date: '2024-02-29',
    paid_at: '2024-02-25T12:00:00Z',
    status: 'paid',
    comment: 'Банковский перевод',
    created_at: '2024-02-01T10:00:00Z',
  },
];

// ============================================================
// СЕРВИС ФУНКЦИИ
// ============================================================

/**
 * Получить все платежи договора
 *
 * @param contractId ID договора
 * @returns Массив платежей
 *
 * ДИЗАЙН: На backend SELECT * FROM payments WHERE contract_id = ? ORDER BY due_date DESC
 */
export async function getPaymentsByContract(contractId: string): Promise<Payment[]> {
  await new Promise(resolve => setTimeout(resolve, 300));

  return MOCK_PAYMENTS.filter(p => p.contract_id === contractId).sort(
    (a, b) => new Date(b.due_date).getTime() - new Date(a.due_date).getTime()
  );
}

/**
 * Получить один платёж по ID
 */
export async function getPaymentById(paymentId: string): Promise<Payment | null> {
  await new Promise(resolve => setTimeout(resolve, 200));

  return MOCK_PAYMENTS.find(p => p.id === paymentId) || null;
}

/**
 * Получить просроченные платежи для арендатора
 *
 * @param tenantId ID арендатора
 * @returns Массив просроченных платежей
 *
 * ДИЗАЙН: На backend JOIN contracts ON payments.contract_id = contracts.id
 * WHERE contracts.tenant_id = ? AND payments.status = 'overdue'
 */
export async function getOverduePayments(_tenantId: string): Promise<Payment[]> {
  await new Promise(resolve => setTimeout(resolve, 350));

  const now = new Date();
  return MOCK_PAYMENTS.filter(p => {
    const dueDate = new Date(p.due_date);
    return dueDate < now && p.paid_at === null;
  });
}

/**
 * Получить статистику платежей для владельца
 *
 * ДИЗАЙН: На backend агрегирующий запрос с GROUP BY contracts.owner_id
 */
export async function getPaymentStats(_ownerId: string): Promise<{
  total_paid: number;
  total_unpaid: number;
  total_overdue: number;
  overdue_count: number;
}> {
  await new Promise(resolve => setTimeout(resolve, 400));

  const stats = {
    total_paid: 0,
    total_unpaid: 0,
    total_overdue: 0,
    overdue_count: 0,
  };

  MOCK_PAYMENTS.forEach(p => {
    if (p.status === 'paid') {
      stats.total_paid += p.amount;
    } else if (p.status === 'unpaid') {
      stats.total_unpaid += p.amount;
    } else if (p.status === 'overdue') {
      stats.total_overdue += p.amount;
      stats.overdue_count += 1;
    }
  });

  return stats;
}

/**
 * Создать новый платёж (для дефолтных ежемесячных платежей)
 *
 * @param contractId ID договора
 * @param dueDate Дата платежа
 * @param amount Сумма
 * @returns Созданный платёж
 *
 * ДИЗАЙН: На backend INSERT INTO payments (...)
 * Обычно это задача планировщика (scheduler), который создаёт платежи
 * в начале месяца на основе active contracts
 */
export async function createPayment(
  contractId: string,
  dueDate: string,
  amount: number
): Promise<Payment> {
  await new Promise(resolve => setTimeout(resolve, 400));

  const newPayment: Payment = {
    id: `payment_${Date.now()}`,
    contract_id: contractId,
    amount,
    due_date: dueDate,
    paid_at: null,
    status: 'unpaid',
    comment: '',
    created_at: new Date().toISOString(),
  };

  MOCK_PAYMENTS.push(newPayment);
  return newPayment;
}

/**
 * Отметить платёж как оплаченный
 *
 * @param paymentId ID платежа
 * @param paidAt Дата оплаты (можно установить текущую)
 * @returns Обновлённый платёж
 *
 * ДИЗАЙН: На backend UPDATE payments SET paid_at = ?, status = 'paid' WHERE id = ?
 */
export async function markPaymentAsPaid(
  paymentId: string,
  paidAt: string = new Date().toISOString()
): Promise<Payment | null> {
  await new Promise(resolve => setTimeout(resolve, 350));

  const payment = MOCK_PAYMENTS.find(p => p.id === paymentId);
  if (!payment) return null;

  payment.paid_at = paidAt;
  payment.status = 'paid';
  return payment;
}

/**
 * Обновить платёж (комментарий, способ оплаты и т.д.)
 */
export async function updatePayment(
  paymentId: string,
  data: Partial<Omit<Payment, 'id' | 'contract_id' | 'created_at'>>
): Promise<Payment | null> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const index = MOCK_PAYMENTS.findIndex(p => p.id === paymentId);
  if (index === -1) return null;

  MOCK_PAYMENTS[index] = {
    ...MOCK_PAYMENTS[index],
    ...data,
  };

  return MOCK_PAYMENTS[index];
}

/**
 * Удалить платёж (редко используется, обычно soft delete)
 */
export async function deletePayment(paymentId: string): Promise<boolean> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const index = MOCK_PAYMENTS.findIndex(p => p.id === paymentId);
  if (index === -1) return false;

  MOCK_PAYMENTS.splice(index, 1);
  return true;
}
