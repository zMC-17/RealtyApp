/**
 * API client placeholder.
 *
 */

export interface ApiClientConfig {
  baseUrl?: string;
  timeout?: number;
}

export class ApiClient {
  constructor(_config: ApiClientConfig = {}) {}

  async get<T>(_endpoint: string): Promise<T> {
    throw new Error('Backend API client is not wired yet');
  }

  async post<T>(_endpoint: string, _data: unknown): Promise<T> {
    throw new Error('Backend API client is not wired yet');
  }

  async put<T>(_endpoint: string, _data: unknown): Promise<T> {
    throw new Error('Backend API client is not wired yet');
  }

  async delete<T>(_endpoint: string): Promise<T> {
    throw new Error('Backend API client is not wired yet');
  }
}

export const apiClient = new ApiClient();
export default apiClient;
