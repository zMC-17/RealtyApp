import api from './api';

import type {
    UserLogin,
    UserCreate,
    Token,
    UserResponse
} from '../types/auth';

export const authService = {
    /**
     * ЗАПРОС К БЭКЕНДУ - логин пользователя
     */
    async login(credentials: UserLogin): Promise<Token> {
        const { data } = await api.post<Token>('/auth/login', credentials);
        return data;
    },

    /**
     * ЗАПРОС К БЭКЕНДУ - регистрация пользователя
     */
    async register(userData: UserCreate): Promise<Token> {
        const { data } = await api.post<Token>('/auth/register', userData);
        return data;
    },

    /**
     * ЗАПРОС К БЭКЕНДУ - получить профиль текущего пользователя
     */
    async getProfile(): Promise<UserResponse> {
        const { data } = await api.get<UserResponse>('/auth/me');
        return data;
    },
};