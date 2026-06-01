// types/property.ts
export interface PropertyResponse {
    id: number;
    owner_id: number;
    title: string;
    address: string;
    description: string | null;
    property_type: string;
}

export interface PropertyCreate {
    title: string;
    address: string;
    description?: string;
    property_type: string;
}

// Заготовленные типы недвижимости
export const PROPERTY_TYPES = [
    { value: 'apartment', label: 'Квартира' },
    { value: 'house', label: 'Дом' },
    { value: 'office', label: 'Офис' },
    { value: 'commercial', label: 'Коммерческое помещение' },
    { value: 'warehouse', label: 'Склад' },
    { value: 'land', label: 'Земельный участок' },
    { value: 'other', label: 'Другое' },
] as const;