import apiClient from './client';

export async function getRequestsByContract(contractId: number): Promise<unknown[]> {
  return apiClient.get<unknown[]>(`/requests/contracts/${contractId}`);
}

export async function getRequestById(requestId: number): Promise<unknown> {
  return apiClient.get<unknown>(`/requests/${requestId}`);
}

export async function getNewRequestsForOwner(): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/requests/owner/me');
}

export async function getActiveRequests(): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/requests/me');
}

export async function createRequest(data: unknown): Promise<unknown> {
  return apiClient.post<unknown>('/requests', data);
}

export async function updateRequestStatus(requestId: number, status: unknown): Promise<unknown> {
  return apiClient.put<unknown>(`/requests/${requestId}`, { status });
}

export async function updateRequest(requestId: number, data: unknown): Promise<unknown> {
  return apiClient.put<unknown>(`/requests/${requestId}`, data);
}

export async function deleteRequest(requestId: number): Promise<boolean> {
  await apiClient.delete(`/requests/${requestId}`);
  return true;
}

export async function getRequestStats(): Promise<unknown> {
  return apiClient.get<unknown>('/requests/owner/me');
}

export default { getRequestsByContract, getRequestById, getNewRequestsForOwner, getActiveRequests, createRequest, updateRequestStatus, updateRequest, deleteRequest, getRequestStats };
