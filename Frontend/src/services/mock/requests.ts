/**
 * Mock сервис для управления заявками на обслуживание/ремонт
 *
 * Симулирует API запросы к /api/requests
 */

import type { Request, RequestStatus } from '../../shared/types';

// ============================================================
// MOCK ДАННЫЕ
// ============================================================

const MOCK_REQUESTS: Request[] = [
  {
    id: 'request_1',
    contract_id: 'contract_1',
    message: 'Не работает горячее водоснабжение',
    status: 'new',
    created_at: '2024-03-20T10:00:00Z',
  },
  {
    id: 'request_2',
    contract_id: 'contract_1',
    message: 'Протекает кран на кухне',
    status: 'in_progress',
    created_at: '2024-03-18T14:30:00Z',
  },
  {
    id: 'request_3',
    contract_id: 'contract_1',
    message: 'Разбилось окно в спальне',
    status: 'completed',
    created_at: '2024-03-15T09:15:00Z',
  },
  {
    id: 'request_4',
    contract_id: 'contract_2',
    message: 'Требуется плановое ТО кондиционера',
    status: 'new',
    created_at: '2024-03-19T11:00:00Z',
  },
];

// ============================================================
// СЕРВИС ФУНКЦИИ
// ============================================================

/**
 * Получить все заявки договора (для арендатора или владельца)
 *
 * @param contractId ID договора
 * @returns Массив заявок
 *
 * ДИЗАЙН: На backend SELECT * FROM requests WHERE contract_id = ? ORDER BY created_at DESC
 */
export async function getRequestsByContract(contractId: string): Promise<Request[]> {
  await new Promise(resolve => setTimeout(resolve, 300));

  return MOCK_REQUESTS.filter(r => r.contract_id === contractId).sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );
}

/**
 * Получить одну заявку по ID
 */
export async function getRequestById(requestId: string): Promise<Request | null> {
  await new Promise(resolve => setTimeout(resolve, 200));

  return MOCK_REQUESTS.find(r => r.id === requestId) || null;
}

/**
 * Получить новые заявки для владельца (все его объекты)
 *
 * ДИЗАЙН: На backend JOIN contracts ON requests.contract_id = contracts.id
 * WHERE contracts.owner_id = ? AND requests.status = 'new'
 * ORDER BY requests.created_at DESC
 */
export async function getNewRequestsForOwner(_ownerId: string): Promise<Request[]> {
  await new Promise(resolve => setTimeout(resolve, 350));

  // В реальной системе это будет JOIN с contracts по owner_id
  const newRequests = MOCK_REQUESTS.filter(r => r.status === 'new');
  return newRequests.sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );
}

/**
 * Получить активные заявки (new + in_progress)
 *
 * ДИЗАЙН: На backend WHERE status IN ('new', 'in_progress')
 */
export async function getActiveRequests(): Promise<Request[]> {
  await new Promise(resolve => setTimeout(resolve, 300));

  return MOCK_REQUESTS.filter(r => r.status === 'new' || r.status === 'in_progress');
}

/**
 * Создать новую заявку (от арендатора)
 *
 * @param contractId ID договора
 * @param message Описание проблемы
 * @returns Созданная заявка
 *
 * ДИЗАЙН: На backend INSERT INTO requests (...)
 * Статус по умолчанию 'new', владелец должен действовать
 */
export async function createRequest(
  contractId: string,
  message: string
): Promise<Request> {
  await new Promise(resolve => setTimeout(resolve, 400));

  const newRequest: Request = {
    id: `request_${Date.now()}`,
    contract_id: contractId,
    message,
    status: 'new',
    created_at: new Date().toISOString(),
  };

  MOCK_REQUESTS.push(newRequest);
  return newRequest;
}

/**
 * Обновить статус заявки
 *
 * @param requestId ID заявки
 * @param status Новый статус
 * @returns Обновлённая заявка
 *
 * ДИЗАЙН: На backend UPDATE requests SET status = ? WHERE id = ?
 * new → in_progress (владелец начал работать)
 * in_progress → completed (работа завершена)
 * completed → new (переоткрыта если проблема не решена)
 */
export async function updateRequestStatus(
  requestId: string,
  status: RequestStatus
): Promise<Request | null> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const request = MOCK_REQUESTS.find(r => r.id === requestId);
  if (!request) return null;

  request.status = status;
  return request;
}

/**
 * Полное обновление заявки
 */
export async function updateRequest(
  requestId: string,
  data: Partial<Omit<Request, 'id' | 'contract_id' | 'created_at'>>
): Promise<Request | null> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const index = MOCK_REQUESTS.findIndex(r => r.id === requestId);
  if (index === -1) return null;

  MOCK_REQUESTS[index] = {
    ...MOCK_REQUESTS[index],
    ...data,
  };

  return MOCK_REQUESTS[index];
}

/**
 * Удалить заявку (редко, обычно только архивирование)
 */
export async function deleteRequest(requestId: string): Promise<boolean> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const index = MOCK_REQUESTS.findIndex(r => r.id === requestId);
  if (index === -1) return false;

  MOCK_REQUESTS.splice(index, 1);
  return true;
}

/**
 * Получить статистику заявок
 *
 * ДИЗАЙН: На backend агрегирующий запрос COUNT(*) GROUP BY status
 */
export async function getRequestStats(): Promise<{
  total: number;
  new: number;
  in_progress: number;
  completed: number;
}> {
  await new Promise(resolve => setTimeout(resolve, 350));

  return {
    total: MOCK_REQUESTS.length,
    new: MOCK_REQUESTS.filter(r => r.status === 'new').length,
    in_progress: MOCK_REQUESTS.filter(r => r.status === 'in_progress').length,
    completed: MOCK_REQUESTS.filter(r => r.status === 'completed').length,
  };
}
