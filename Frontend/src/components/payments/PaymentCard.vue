<!-- components/payments/PaymentCard.vue -->
<template>
    <div class="payment-row" :class="{
        'payment-row--waiting': payment.status === 'waiting_confirmation',
        'payment-row--overdue': payment.status === 'overdue',
    }">
        <!-- Левый акцент-цвет (вертикальная полоска) -->
        <div class="row-accent"></div>

        <!-- Статус + дата -->
        <div class="row-status">
            <PaymentStatusBadge :status="payment.status" />
            <span class="row-date">{{ formattedDate }}</span>
        </div>

        <!-- Объект -->
        <div class="row-property">
            <span class="row-meta-label">Объект</span>
            <span class="row-meta-value">{{ payment.property_info?.title || '—' }}</span>
        </div>

        <!-- Арендатор -->
        <div class="row-tenant">
            <span class="row-meta-label">Арендатор</span>
            <span class="row-meta-value">{{ payment.tenant_info?.name || '—' }}</span>
        </div>

        <!-- Сумма -->
        <div class="row-amount">
            {{ formattedAmount }}
        </div>

        <!-- Кнопки — только для waiting_confirmation -->
        <div v-if="payment.status === 'waiting_confirmation'" class="row-actions">
            <button class="action-btn action-btn--confirm" @click.stop="$emit('confirm', payment.id)"
                title="Подтвердить">
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <path d="M2 7l3 3 6-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
                        stroke-linejoin="round" />
                </svg>
            </button>
            <button class="action-btn action-btn--reject" @click.stop="$emit('reject', payment.id)" title="Отклонить">
                <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                    <path d="M1 1l9 9M10 1L1 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                </svg>
            </button>
        </div>

        <!-- Заглушка по ширине когда кнопок нет -->
        <div v-else class="row-actions-placeholder"></div>

    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PaymentResponse } from '../../types/payment';
import PaymentStatusBadge from './PaymentStatusBadge.vue';

const props = defineProps<{ payment: PaymentResponse }>();
defineEmits<{ confirm: [id: number]; reject: [id: number] }>();

const formattedAmount = computed(() =>
    new Intl.NumberFormat('ru-RU', {
        style: 'currency', currency: 'RUB', minimumFractionDigits: 0,
    }).format(parseFloat(props.payment.amount))
);

const formattedDate = computed(() =>
    new Date(props.payment.due_date).toLocaleDateString('ru-RU', {
        day: 'numeric', month: 'short', year: 'numeric',
    })
);
</script>

<style scoped>
/*
  Горизонтальная строка-запись:
  [полоска] [статус+дата] [объект] [арендатор] [сумма] [кнопки]
  Выглядит как строка в банковской выписке.
*/
.payment-row {
    display: grid;
    grid-template-columns: 3px 160px 1fr 1fr auto 72px;
    align-items: center;
    gap: var(--space-4);

    background: rgba(255, 255, 255, 0.50);
    backdrop-filter: blur(16px) saturate(130%);
    -webkit-backdrop-filter: blur(16px) saturate(130%);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: var(--radius-md);
    padding: var(--space-4) var(--space-5) var(--space-4) 0;
    overflow: hidden;

    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.65) inset, 0 2px 8px rgba(28, 26, 23, 0.05);
    transition: box-shadow var(--transition), border-color var(--transition);
}

.payment-row:hover {
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.80) inset, 0 6px 20px rgba(28, 26, 23, 0.09);
    border-color: rgba(255, 255, 255, 0.82);
}

/* ---- Левая полоска-акцент ---- */
.row-accent {
    height: 100%;
    min-height: 52px;
    border-radius: 0 2px 2px 0;
    background: transparent;
    transition: background var(--transition);
}

.payment-row--waiting .row-accent {
    background: var(--color-info);
}

.payment-row--overdue .row-accent {
    background: var(--color-danger);
}

/* ---- Статус + дата ---- */
.row-status {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
    min-width: 0;
}

.row-date {
    font-size: var(--text-xs);
    color: var(--color-dark-35);
    font-weight: 500;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}

/* ---- Мета-ячейки (объект, арендатор) ---- */
.row-property,
.row-tenant {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
}

.row-meta-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--color-dark-35);
}

.row-meta-value {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--color-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ---- Сумма ---- */
.row-amount {
    font-size: var(--text-lg);
    font-weight: 800;
    color: var(--color-emerald);
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    text-align: right;
}

/* ---- Кнопки действий ---- */
.row-actions {
    display: flex;
    gap: var(--space-2);
    justify-content: flex-end;
}

.row-actions-placeholder {
    width: 72px;
}

.action-btn {
    width: 30px;
    height: 30px;
    border-radius: var(--radius-sm);
    border: 1px solid transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all var(--transition);
    flex-shrink: 0;
}

.action-btn--confirm {
    background: var(--color-success-bg);
    border-color: rgba(26, 107, 74, 0.20);
    color: var(--color-emerald);
}

.action-btn--confirm:hover {
    background: var(--color-emerald);
    color: #fff;
    border-color: var(--color-emerald);
    box-shadow: 0 3px 10px rgba(26, 107, 74, 0.30);
}

.action-btn--reject {
    background: var(--color-danger-bg);
    border-color: rgba(185, 64, 64, 0.18);
    color: var(--color-danger);
}

.action-btn--reject:hover {
    background: var(--color-danger);
    color: #fff;
    border-color: var(--color-danger);
    box-shadow: 0 3px 10px rgba(185, 64, 64, 0.25);
}
</style>