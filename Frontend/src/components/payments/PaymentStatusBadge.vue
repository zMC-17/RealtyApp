<!-- components/payments/PaymentStatusBadge.vue -->
<template>
    <span class="status-badge" :class="`status-badge--${status}`">
        {{ label }}
    </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PaymentStatus } from '../../types/payment';
import { PAYMENT_STATUS_LABELS } from '../../types/payment';

const props = defineProps<{ status: PaymentStatus }>();
const label = computed(() => PAYMENT_STATUS_LABELS[props.status]);
</script>

<style scoped>
.status-badge {
    display: inline-flex;
    align-items: center;
    padding: 3px var(--space-3);
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    white-space: nowrap;
}

.status-badge--pending {
    background: var(--color-warning-bg);
    color: var(--color-warning);
}

.status-badge--waiting_confirmation {
    background: var(--color-info-bg);
    color: var(--color-info);
}

.status-badge--overdue {
    background: var(--color-danger-bg);
    color: var(--color-danger);
}

.status-badge--paid {
    background: var(--color-success-bg);
    color: var(--color-success);
}
</style>