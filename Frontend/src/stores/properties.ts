/**
 * Pinia хранилище для управления недвижимостью
 *
 * Управляет состоянием списка объектов недвижимости владельца:
 * - Кэширование данных из mock сервиса
 * - Loading/error состояния
 * - Простые операции CRUD
 *
 * Готово для замены на реальный API
 */

import { defineStore } from 'pinia';
import { ref } from 'vue';
import {
  getPropertiesByOwner,
  createProperty,
  updateProperty,
  deleteProperty,
} from '../services/mock/properties';
import type { Property } from '../shared/types';

export const usePropertiesStore = defineStore('properties', () => {
  // State
  const properties = ref<Property[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // ============================================================
  // Actions
  // ============================================================

  /**
   * Загрузить список недвижимости владельца
   */
  const fetchProperties = async (ownerId: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const data = await getPropertiesByOwner(ownerId);
      properties.value = data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки недвижимости';
      properties.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Добавить новый объект недвижимости
   */
  const addProperty = async (
    ownerId: string,
    data: Omit<Property, 'id' | 'owner_id' | 'created_at'>
  ) => {
    try {
      const newProperty = await createProperty(ownerId, data);
      properties.value.push(newProperty);
      return newProperty;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка создания объекта';
      throw err;
    }
  };

  /**
   * Обновить объект недвижимости
   */
  const editProperty = async (
    propertyId: string,
    data: Partial<Omit<Property, 'id' | 'owner_id' | 'created_at'>>
  ) => {
    try {
      const updated = await updateProperty(propertyId, data);
      const index = properties.value.findIndex(p => p.id === propertyId);
      if (index >= 0) {
        properties.value[index] = updated;
      }
      return updated;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка обновления объекта';
      throw err;
    }
  };

  /**
   * Удалить объект недвижимости
   */
  const removeProperty = async (propertyId: string) => {
    try {
      await deleteProperty(propertyId);
      properties.value = properties.value.filter(p => p.id !== propertyId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка удаления объекта';
      throw err;
    }
  };

  /**
   * Очистить состояние
   */
  const reset = () => {
    properties.value = [];
    error.value = null;
    isLoading.value = false;
  };

  return {
    // State
    properties,
    isLoading,
    error,

    // Actions
    fetchProperties,
    addProperty,
    editProperty,
    removeProperty,
    reset,
  };
});
