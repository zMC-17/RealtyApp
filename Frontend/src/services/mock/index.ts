/**
 * Mock API сервисы
 *
 * Объединённый экспорт всех mock сервисов для работы с доменами
 * В production это будет заменено на реальные HTTP API запросы
 */

// Сервис для управления объектами недвижимости
export * as propertiesService from './properties';

// Сервис для управления договорами
export * as contractsService from './contracts';

// Сервис для управления платежами
export * as paymentsService from './payments';

// Сервис для управления заявками
export * as requestsService from './requests';

// Сервис для пользователей
export * as usersService from './users';

/**
 * Использование в компонентах:
 *
 * import { propertiesService, contractsService } from '@/services/mock'
 *
 * // Получить свойства владельца
 * const properties = await propertiesService.getPropertiesByOwner(ownerId)
 *
 * // Получить договоры
 * const contracts = await contractsService.getContractsByOwner(ownerId)
 *
 * // Создать платёж
 * const payment = await paymentsService.createPayment(contractId, dueDate, amount)
 *
 * // Создать заявку
 * const request = await requestsService.createRequest(contractId, message)
 */
