<!-- components/payments/PaymentStatusBadge.vue -->
<template>
    <span class="status-badge" :style="{ backgroundColor: bgColor }">
        <span class="status-icon">{{ icon }}</span>
        {{ label }}
    </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PaymentStatus } from '../../types/payment';
import { PAYMENT_STATUS_LABELS, PAYMENT_STATUS_COLORS } from '../../types/payment';

const props = defineProps<{
    status: PaymentStatus;
}>();

const label = computed(() => PAYMENT_STATUS_LABELS[props.status]);
const bgColor = computed(() => PAYMENT_STATUS_COLORS[props.status]);

const icon = computed(() => {
    const icons: Record<PaymentStatus, string> = {
        pending: '⏳',
        waiting_confirmation: '🔍',
        overdue: '⚠️',
        paid: '✅',
    };
    return icons[props.status];
});
</script>

<style scoped>
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    color: white;
    font-size: 0.8rem;
    font-weight: 500;
    white-space: nowrap;
}

.status-icon {
    font-size: 0.9rem;
}
</style>