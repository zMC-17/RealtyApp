import apiClient from './client';

export async function getContractsByOwner(): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/contracts/owner/me');
}

export async function getContractsByTenant(): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/contracts/tenant/me');
}

export async function getContractById(contractId: number): Promise<unknown> {
  return apiClient.get<unknown>(`/contracts/${contractId}`);
}

export async function createContract(data: unknown): Promise<unknown> {
  return apiClient.post<unknown>('/contracts', data);
}

export async function updateContract(contractId: number, data: unknown): Promise<unknown> {
  return apiClient.put<unknown>(`/contracts/${contractId}`, data);
}

export async function updateContractStatus(contractId: number, status: unknown): Promise<unknown> {
  return apiClient.put<unknown>(`/contracts/${contractId}`, { status });
}

export async function deleteContract(contractId: number): Promise<boolean> {
  await apiClient.delete(`/contracts/${contractId}`);
  return true;
}

export default { getContractsByOwner, getContractsByTenant, getContractById, createContract, updateContract, updateContractStatus, deleteContract };
