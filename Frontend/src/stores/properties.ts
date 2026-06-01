// stores/properties.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { propertiesService } from '../services/properties';
import type { PropertyResponse, PropertyCreate } from '../types/property';

export const usePropertiesStore = defineStore('properties', () => {
    // ===== Состояние =====
    const properties = ref<PropertyResponse[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const currentProperty = ref<PropertyResponse | null>(null);

    // ===== Геттеры =====
    const hasProperties = computed(() => properties.value.length > 0);
    const propertiesCount = computed(() => properties.value.length);

    // ===== Действия =====
    /**
     * Загрузить список объектов
     */
    async function fetchProperties() {
        loading.value = true;
        error.value = null;

        try {
            const data = await propertiesService.getMyProperties();
            properties.value = data;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка загрузки объектов';
            console.error('Ошибка загрузки объектов:', err);
        } finally {
            loading.value = false;
        }
    }

    /**
     * Загрузить один объект
     */
    async function fetchProperty(id: number) {
        loading.value = true;
        error.value = null;

        try {
            const data = await propertiesService.getProperty(id);
            currentProperty.value = data;
            return data;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка загрузки объекта';
            console.error('Ошибка загрузки объекта:', err);
            return null;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Создать новый объект
     */
    async function createProperty(propertyData: PropertyCreate) {
        loading.value = true;
        error.value = null;

        try {
            const newProperty = await propertiesService.createProperty(propertyData);
            // Добавляем новый объект в начало списка
            properties.value.unshift(newProperty);
            return newProperty;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Ошибка создания объекта';
            console.error('Ошибка создания объекта:', err);
            return null;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Сбросить ошибку
     */
    function clearError() {
        error.value = null;
    }

    return {
        // Состояние
        properties,
        loading,
        error,
        currentProperty,

        // Геттеры
        hasProperties,
        propertiesCount,

        // Действия
        fetchProperties,
        fetchProperty,
        createProperty,
        clearError,
    };
});