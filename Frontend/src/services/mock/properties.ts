/**
 * Mock сервис для управления объектами недвижимости
 *
 * Симулирует API запросы к /api/properties
 * При интеграции с backend просто замените функции на реальные API запросы
 */

import type { Property } from '../../shared/types';

// ============================================================
// MOCK ДАННЫЕ
// ============================================================

const MOCK_PROPERTIES: Property[] = [
  {
    id: 'prop_1',
    owner_id: 'user_1',
    title: 'Уютная квартира в центре',
    address: 'Москва, ул. Тверская, 1',
    description: 'Двухкомнатная квартира с видом на город. Мебель, интернет включены.',
    property_type: 'apartment',
    created_at: '2024-01-15T10:00:00Z',
  },
  {
    id: 'prop_2',
    owner_id: 'user_1',
    title: 'Коттедж за городом',
    address: 'Московская область, Кубинка',
    description: 'Трёхэтажный коттедж с участком. Гараж, баня, бассейн.',
    property_type: 'house',
    created_at: '2024-02-20T14:30:00Z',
  },
  {
    id: 'prop_3',
    owner_id: 'user_2',
    title: 'Комната в коммунальной квартире',
    address: 'Санкт-Петербург, пр. Литейный, 45',
    description: 'Уютная комната с собственным входом. Ремонт, окна на улицу.',
    property_type: 'room',
    created_at: '2024-03-10T09:15:00Z',
  },
  {
    id: 'prop_4',
    owner_id: 'user_2',
    title: 'Офисное помещение',
    address: 'Санкт-Петербург, ул. Невского, 12',
    description: 'Коммерческое помещение 50м². Отличное расположение для магазина или офиса.',
    property_type: 'commercial',
    created_at: '2024-01-05T11:00:00Z',
  },
];

// ============================================================
// СЕРВИС ФУНКЦИИ
// ============================================================

/**
 * Получить все объекты недвижимости владельца
 *
 * @param ownerId ID владельца
 * @returns Массив объектов
 *
 * ДИЗАЙН: На backend будет SQL запрос WHERE owner_id = ?
 */
export async function getPropertiesByOwner(ownerId: string): Promise<Property[]> {
  // Симулируем задержку сети
  await new Promise(resolve => setTimeout(resolve, 300));

  // Фильтруем по владельцу
  return MOCK_PROPERTIES.filter(p => p.owner_id === ownerId);
}

/**
 * Получить один объект по ID
 *
 * @param propertyId ID объекта
 * @returns Данные объекта или null
 *
 * ДИЗАЙН: На backend GET /api/properties/:id
 */
export async function getPropertyById(propertyId: string): Promise<Property | null> {
  await new Promise(resolve => setTimeout(resolve, 200));

  const property = MOCK_PROPERTIES.find(p => p.id === propertyId);
  return property || null;
}

/**
 * Создать новый объект недвижимости
 *
 * @param ownerId ID владельца
 * @param data Данные объекта (без id и created_at)
 * @returns Созданный объект с id и created_at
 *
 * ДИЗАЙН: На backend POST /api/properties
 * Сервер генерирует id (UUID) и created_at
 */
export async function createProperty(
  ownerId: string,
  data: Omit<Property, 'id' | 'owner_id' | 'created_at'>
): Promise<Property> {
  await new Promise(resolve => setTimeout(resolve, 400));

  // Генерируем mock ID
  const newProperty: Property = {
    id: `prop_${Date.now()}`,
    owner_id: ownerId,
    ...data,
    created_at: new Date().toISOString(),
  };

  MOCK_PROPERTIES.push(newProperty);
  return newProperty;
}

/**
 * Обновить объект недвижимости
 *
 * @param propertyId ID объекта
 * @param data Поля для обновления
 * @returns Обновлённый объект
 *
 * ДИЗАЙН: На backend PUT /api/properties/:id
 */
export async function updateProperty(
  propertyId: string,
  data: Partial<Omit<Property, 'id' | 'owner_id' | 'created_at'>>
): Promise<Property | null> {
  await new Promise(resolve => setTimeout(resolve, 350));

  const index = MOCK_PROPERTIES.findIndex(p => p.id === propertyId);
  if (index === -1) return null;

  MOCK_PROPERTIES[index] = {
    ...MOCK_PROPERTIES[index],
    ...data,
  };

  return MOCK_PROPERTIES[index];
}

/**
 * Удалить объект недвижимости
 *
 * @param propertyId ID объекта
 * @returns true если удалён, false если не найден
 *
 * ДИЗАЙН: На backend DELETE /api/properties/:id
 * Может быть soft delete (marked as deleted) в реальной системе
 */
export async function deleteProperty(propertyId: string): Promise<boolean> {
  await new Promise(resolve => setTimeout(resolve, 300));

  const index = MOCK_PROPERTIES.findIndex(p => p.id === propertyId);
  if (index === -1) return false;

  MOCK_PROPERTIES.splice(index, 1);
  return true;
}
