/**
 * Базовый API клиент для отправки запросов
 *
 * Этот клиент абстрагирует логику сетевых запросов и может быть легко
 * заменён на реальный HTTP клиент (fetch/axios) при интеграции с backend
 */

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface ApiClientConfig {
  baseUrl?: string;
  timeout?: number;
  delay?: number;
}

/**
 * ApiClient - базовый клиент для работы с API
 *
 * В production переключится на реальные HTTP запросы, но интерфейс останется
 * тем же, что позволяет не менять код приложения
 */
export class ApiClient {
  private delay: number;

  constructor(config: ApiClientConfig = {}) {
    // Зарезервировано для будущей интеграции с реальным HTTP клиентом
    // const _baseUrl = config.baseUrl || '';
    // const _timeout = config.timeout || 30000;
    this.delay = config.delay || 300; // Симулируем задержку сети
  }

  /**
   * GET запрос
   */
  async get<T>(_endpoint: string, options?: { delay?: number }): Promise<T> {
    const delayMs = options?.delay ?? this.delay;
    await this.sleep(delayMs);
    // В production: return fetch(`${baseUrl}${_endpoint}`).then(r => r.json())
    throw new Error('Not implemented: Use mock service instead');
  }

  /**
   * POST запрос
   */
  async post<T>(
    _endpoint: string,
    _data: unknown,
    options?: { delay?: number }
  ): Promise<T> {
    const delayMs = options?.delay ?? this.delay;
    await this.sleep(delayMs);
    // В production: return fetch(...).then(r => r.json())
    throw new Error('Not implemented: Use mock service instead');
  }

  /**
   * PUT запрос
   */
  async put<T>(
    _endpoint: string,
    _data: unknown,
    options?: { delay?: number }
  ): Promise<T> {
    const delayMs = options?.delay ?? this.delay;
    await this.sleep(delayMs);
    throw new Error('Not implemented: Use mock service instead');
  }

  /**
   * DELETE запрос
   */
  async delete<T>(_endpoint: string, options?: { delay?: number }): Promise<T> {
    const delayMs = options?.delay ?? this.delay;
    await this.sleep(delayMs);
    throw new Error('Not implemented: Use mock service instead');
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export const apiClient = new ApiClient({ delay: 300 });
