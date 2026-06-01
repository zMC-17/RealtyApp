import apiClient from './client';

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface AuthProfile {
  id: number;
  name: string;
  email: string;
}

export async function login(payload: LoginPayload): Promise<AuthToken> {
  return apiClient.post<AuthToken>('/auth/login', payload);
}

export async function register(payload: RegisterPayload): Promise<AuthToken> {
  return apiClient.post<AuthToken>('/auth/register', payload);
}

export async function me(): Promise<AuthProfile> {
  return apiClient.get<AuthProfile>('/auth/me');
}

export default { login, register, me };
