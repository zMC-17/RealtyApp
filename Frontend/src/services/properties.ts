// services/properties.service.ts
import api from './api';
import type { PropertyResponse, PropertyCreate } from '../types/property';

export const propertiesService = {
    /**
     * Получить все объекты текущего владельца
     */
    async getMyProperties(): Promise<PropertyResponse[]> {
        const { data } = await api.get<PropertyResponse[]>('/properties/me');
        return data;
    },

    /**
     * Получить один объект по ID
     */
    async getProperty(id: number): Promise<PropertyResponse> {
        const { data } = await api.get<PropertyResponse>(`/properties/${id}`);
        return data;
    },

    /**
     * Создать новый объект
     */
    async createProperty(property: PropertyCreate): Promise<PropertyResponse> {
        const { data } = await api.post<PropertyResponse>('/properties', property);
        return data;
    },

    /**
     * Обновить объект (понадобится позже)
     */
    async updateProperty(id: number, property: Partial<PropertyCreate>): Promise<PropertyResponse> {
        const { data } = await api.put<PropertyResponse>(`/properties/${id}`, property);
        return data;
    },

    /**
     * Удалить объект (понадобится позже)
     */
    async deleteProperty(id: number): Promise<void> {
        await api.delete(`/properties/${id}`);
    },
};