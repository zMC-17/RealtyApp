import apiClient from './client';

export async function getUserById(userId: number): Promise<unknown> {
  return apiClient.get<unknown>(`/users/${userId}`);
}

export async function getUsersByIds(_userIds: number[]): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/users');
}

export async function getTenants(): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/users');
}

export default { getUserById, getUsersByIds, getTenants };
