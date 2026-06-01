/*
* Сессия для храниения ролей
*/

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useRoleStore = defineStore('role', () => {

    type UserRole = 'landlord' | 'tenant'
    const STORAGE_KEY = 'user_role'

    // Пытаемся загрузить сохранённую роль из localStorage при инициализации
    const savedRole = localStorage.getItem(STORAGE_KEY) as UserRole | null;

    // ===== Состояния =====
    const role = ref<UserRole>(savedRole || 'landlord')

    // ===== Геттеры ======
    const getRole = computed(() => role.value)

    // ===== Действия =====
    const setRole = (newRole: UserRole) => {
        role.value = newRole
        // Обновляем локальное хранилище при изменении роли
        localStorage.setItem(STORAGE_KEY, newRole)
    }

    return {
        getRole,
        setRole,
    }

})