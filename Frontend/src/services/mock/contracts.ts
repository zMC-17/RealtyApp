/**
 * Mock сервис для управления договорами аренды
 *
 * Симулирует API запросы к /api/contracts
 */

import type { Contract, ContractStatus } from '../../shared/types';

// ============================================================
// MOCK ДАННЫЕ
// ============================================================

const MOCK_CONTRACTS: Contract[] = [
  {
    id: 'contract_1',
    property_id: 'prop_1',
    tenant_id: 'user_3',
    start_date: '2024-01-01',
    end_date: '2025-01-01',
    monthly_payment: 50000,
    status: 'active',
    created_at: '2023-12-15T10:00:00Z',
  },
  {
    id: 'contract_2',
    property_id: 'prop_2',
    tenant_id: 'user_4',
    start_date: '2024-02-01',
    end_date: '2026-02-01',
    monthly_payment: 150000,
    status: 'active',
    created_at: '2024-01-20T14:30:00Z',
  },
  {
    id: 'contract_3',
    property_id: 'prop_3',
    tenant_id: 'user_5',
    start_date: '2024-03-15',
    end_date: '2024-09-15',
    monthly_payment: 20000,
    status: 'pending',
    created_at: '2024-03-01T09:15:00Z',
  },
];

// ============================================================
// СЕРВИС ФУНКЦИИ
// ============================================================

/**
 * Получить все договоры владельца (по его объектам)
 *
 * @param ownerId ID владельца
 * @returns Массив договоров
 *
 * ДИЗАЙН: JOIN с Property таблицей где owner_id = ?
 */
export async function getContractsByOwner(ownerId: string): Promise<Contract[]> {
  await new Promise(resolve => setTimeout(resolve, 350));

  // В реальной системе это будет JOIN contracts ON properties.owner_id = ?
  // Здесь симулируем сопоставление owner_id -> property_id.
  const ownerPropertyMap: Record<string, string[]> = {
    user_1: ['prop_1', 'prop_2'],
    user_2: ['prop_3', 'prop_4'],
  };

  const ownerPropertyIds = ownerPropertyMap[ownerId] ?? [];
  return MOCK_CONTRACTS.filter(contract => ownerPropertyIds.includes(contract.property_id));
}

/**
 * Получить все договоры арендатора
 *
 * @param tenantId ID арендатора
 * @returns Массив договоров
 *
 * ДИЗАЙН: На backend SELECT * FROM contracts WHERE tenant_id = ?
 */
export async function getContractsByTenant(tenantId: string): Promise<Contract[]> {
  await new Promise(resolve => setTimeout(resolve, 300));

  return MOCK_CONTRACTS.filter(c => c.tenant_id === tenantId);
}

/**
 * Получить один договор по ID
 */
export async function getContractById(contractId: string): Promise<Contract | null> {
  await new Promise(resolve => setTimeout(resolve, 200));

  return MOCK_CONTRACTS.find(c => c.id === contractId) || null;
}

/**
 * Создать новый договор
 *
 * @param data Данные договора
 * @returns Созданный договор
 *
 * ДИЗАЙН: На backend INSERT INTO contracts (...)
 * Сервер генерирует id и created_at
 */
export async function createContract(
  data: Omit<Contract, 'id' | 'created_at'>
): Promise<Contract> {
  await new Promise(resolve => setTimeout(resolve, 400));

  const newContract: Contract = {
    id: `contract_${Date.now()}`,
    ...data,
    created_at: new Date().toISOString(),
  };

  MOCK_CONTRACTS.push(newContract);
  return newContract;
}

/**
 * Обновить договор
 *
 * @param contractId ID договора
 * @param data Поля для обновления
 * @returns Обновлённый договор
 *
 * ДИЗАЙН: На backend UPDATE contracts SET ... WHERE id = ?
 */
export async function updateContract(
  contractId: string,
  data: Partial<Omit<Contract, 'id' | 'created_at'>>
): Promise<Contract | null> {
  await new Promise(resolve => setTimeout(resolve, 350));

  const index = MOCK_CONTRACTS.findIndex(c => c.id === contractId);
  if (index === -1) return null;

  MOCK_CONTRACTS[index] = {
    ...MOCK_CONTRACTS[index],
    ...data,
  };

  return MOCK_CONTRACTS[index];
}

/**
 * Изменить статус договора
 *
 * @param contractId ID договора
 * @param status Новый статус
 * @returns Обновлённый договор
 *
 * ДИЗАЙН: Частная функция, так как status имеет специальную бизнес-логику
 */
export async function updateContractStatus(
  contractId: string,
  status: ContractStatus
): Promise<Contract | null> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const contract = MOCK_CONTRACTS.find(c => c.id === contractId);
  if (!contract) return null;

  // Можно добавить валидацию переходов статусов:
  // pending → active (после подписания)
  // active → terminated (расторжение)
  // и т.д.

  contract.status = status;
  return contract;
}

/**
 * Удалить договор
 */
export async function deleteContract(contractId: string): Promise<boolean> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const index = MOCK_CONTRACTS.findIndex(c => c.id === contractId);
  if (index === -1) return false;

  MOCK_CONTRACTS.splice(index, 1);
  return true;
}
