// services/contracts.service.ts
import api from './api';
import type { ContractResponse, ContractCreateByEmail } from '../types/contract';

export const contractsService = {
    async getOwnerContracts(): Promise<ContractResponse[]> {
        const { data } = await api.get<ContractResponse[]>('/contracts/owner/me');
        return data;
    },

    async getContract(id: number): Promise<ContractResponse> {
        const { data } = await api.get<ContractResponse>(`/contracts/${id}`);
        return data;
    },

    async createByEmail(payload: ContractCreateByEmail): Promise<ContractResponse> {
        const { data } = await api.post<ContractResponse>('/contracts/by-email', payload);
        return data;
    },
    // services/contracts.service.ts — добавьте

    async getTenantContracts(): Promise<ContractWithDetails[]> {
        const { data } = await api.get<ContractWithDetails[]>('/contracts/tenant/me');
        return data;
    },

    async confirmContract(contractId: number): Promise<ContractResponse> {
        const { data } = await api.post<ContractResponse>(`/contracts/${contractId}/confirm`);
        return data;
    },
};