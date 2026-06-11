<template>
  <div class="stat-card">
    <div class="stat-label">{{ label }}</div>
    <div class="stat-value" :class="{ 'stat-value--currency': isCurrency }">
      {{ displayValue }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  label: string;
  value: number | string;
  color?: string;
  icon?:  string;
}>();

const isCurrency   = computed(() => typeof props.value === 'string' && props.value.includes('₽'));
const displayValue = computed(() => props.value);
</script>

<style scoped>
.stat-card {
  /* Стекло поверх blob-фона лейаута */
  background: rgba(255, 255, 255, 0.52);
  backdrop-filter: blur(20px) saturate(140%);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  border: 1px solid rgba(255, 255, 255, 0.65);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  position: relative;
  overflow: hidden;
  box-shadow:
    0 2px 0 rgba(255,255,255,0.70) inset,
    0 8px 32px rgba(28, 26, 23, 0.07);
  transition: box-shadow var(--transition), border-color var(--transition);
}

/* Верхняя акцентная линия появляется при hover */
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--color-emerald), var(--color-olive));
  opacity: 0;
  transition: opacity var(--transition);
}

.stat-card:hover {
  box-shadow:
    0 2px 0 rgba(255,255,255,0.80) inset,
    0 12px 40px rgba(28, 26, 23, 0.11);
  border-color: rgba(255,255,255,0.80);
}

.stat-card:hover::before { opacity: 1; }

.stat-label {
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--color-dark-35);
}

.stat-value {
  font-size: var(--text-3xl);
  font-weight: 800;
  color: var(--color-dark);
  line-height: 1;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}

.stat-value--currency {
  font-size: var(--text-2xl);
  color: var(--color-emerald);
}
</style>