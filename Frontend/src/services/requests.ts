// services/requests.service.ts
import api from './api';
import type { RequestWithDetails, RequestCreate } from '../types/request';

export const requestsService = {
    async getTenantRequests(): Promise<RequestWithDetails[]> {
        const { data } = await api.get<RequestWithDetails[]>('/requests/tenant/me');
        return data;
    },

    async getOwnerRequests(): Promise<RequestWithDetails[]> {
        const { data } = await api.get<RequestWithDetails[]>('/requests/owner/me');
        return data;
    },

    async createRequest(payload: RequestCreate): Promise<RequestWithDetails> {
        const { data } = await api.post<RequestWithDetails>('/requests', payload);
        return data;
    },

    async updateRequestStatus(requestId: number, status: string): Promise<RequestWithDetails> {
        const { data } = await api.put<RequestWithDetails>(`/requests/${requestId}`, { status });
        return data;
    },
    async getContractRequests(contractId: number): Promise<RequestWithDetails[]> {
        const { data } = await api.get<RequestWithDetails[]>(`/requests/contracts/${contractId}`);
        return data;
    },
};