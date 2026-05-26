/**
 * Mock сервис для пользователей
 *
 * Нужен для отображения tenant username и подготовки интеграции с backend /api/users.
 */

import type { User } from '../../shared/types';

const MOCK_USERS: User[] = [
  {
    id: 'user_1',
    email: 'owner1@realty.app',
    username: 'landlord_ivanov',
    password_hash: 'hashed_password_1',
    created_at: '2023-11-01T09:00:00Z',
  },
  {
    id: 'user_2',
    email: 'owner2@realty.app',
    username: 'landlord_petrova',
    password_hash: 'hashed_password_2',
    created_at: '2023-11-15T11:20:00Z',
  },
  {
    id: 'user_3',
    email: 'tenant1@realty.app',
    username: 'tenant_smirnov',
    password_hash: 'hashed_password_3',
    created_at: '2024-01-01T08:10:00Z',
  },
  {
    id: 'user_4',
    email: 'tenant2@realty.app',
    username: 'tenant_orlova',
    password_hash: 'hashed_password_4',
    created_at: '2024-01-10T12:40:00Z',
  },
  {
    id: 'user_5',
    email: 'tenant3@realty.app',
    username: 'tenant_romanov',
    password_hash: 'hashed_password_5',
    created_at: '2024-02-02T14:00:00Z',
  },
];

export async function getUserById(userId: string): Promise<User | null> {
  await new Promise(resolve => setTimeout(resolve, 180));
  return MOCK_USERS.find(user => user.id === userId) ?? null;
}

export async function getUsersByIds(userIds: string[]): Promise<User[]> {
  await new Promise(resolve => setTimeout(resolve, 220));
  const unique = new Set(userIds);
  return MOCK_USERS.filter(user => unique.has(user.id));
}

/**
 * Получить арендаторов для выбора в форме договора
 *
 * ДИЗАЙН: На backend это будет endpoint с ролью,
 * например GET /api/users?role=tenant.
 */
export async function getTenants(): Promise<User[]> {
  await new Promise(resolve => setTimeout(resolve, 220));

  // В mock-версии считаем арендаторами пользователей, чей username начинается с tenant_.
  return MOCK_USERS.filter(user => user.username.startsWith('tenant_'));
}
