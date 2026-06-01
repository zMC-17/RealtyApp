import apiClient from './client';

export async function getPropertiesByOwner(): Promise<unknown[]> {
  return apiClient.get<unknown[]>('/properties/me');
}

export async function getPropertyById(propertyId: number): Promise<unknown> {
  return apiClient.get<unknown>(`/properties/${propertyId}`);
}

export async function createProperty(data: unknown): Promise<unknown> {
  return apiClient.post<unknown>('/properties', data);
}

export async function updateProperty(propertyId: number, data: unknown): Promise<unknown> {
  return apiClient.put<unknown>(`/properties/${propertyId}`, data);
}

export async function deleteProperty(propertyId: number): Promise<boolean> {
  await apiClient.delete(`/properties/${propertyId}`);
  return true;
}

export default { getPropertiesByOwner, getPropertyById, createProperty, updateProperty, deleteProperty };
