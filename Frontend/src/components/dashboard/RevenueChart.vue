<!-- components/dashboard/RevenueChart.vue -->
<template>
    <div class="chart-wrap">
        <!-- Метки оси Y -->
        <div class="y-axis">
            <span v-for="tick in yTicks" :key="tick" class="y-tick">{{ formatTick(tick) }}</span>
        </div>

        <!-- SVG-область графика -->
        <div class="chart-area" ref="chartAreaRef">
            <svg v-if="points.length" :viewBox="`0 0 ${SVG_W} ${SVG_H}`" preserveAspectRatio="none" class="chart-svg">
                <defs>
                    <!-- Градиент-заливка под линией -->
                    <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="var(--color-emerald)" stop-opacity="0.18" />
                        <stop offset="100%" stop-color="var(--color-emerald)" stop-opacity="0" />
                    </linearGradient>
                </defs>

                <!-- Горизонтальные направляющие -->
                <g class="grid">
                    <line v-for="tick in yTicks" :key="tick" x1="0" :y1="yPos(tick)" :x2="SVG_W" :y2="yPos(tick)"
                        stroke="var(--color-dark-12)" stroke-width="1" />
                </g>

                <!-- Заливка под линией -->
                <path :d="areaPath" fill="url(#areaGrad)" />

                <!-- Основная линия -->
                <polyline :points="polylinePoints" fill="none" stroke="var(--color-emerald)" stroke-width="2"
                    stroke-linejoin="round" stroke-linecap="round" />

                <!-- Квадратные маркеры + тултип-зоны -->
                <g v-for="(p, i) in points" :key="i">
                    <!-- Прозрачная зона для hover -->
                    <rect :x="p.x - 20" :y="0" width="40" :height="SVG_H" fill="transparent"
                        @mouseenter="hoveredIndex = i" @mouseleave="hoveredIndex = null" class="hover-zone" />
                    <!-- Квадратный маркер -->
                    <rect :x="p.x - 4" :y="p.y - 4" width="8" height="8"
                        :fill="hoveredIndex === i ? 'var(--color-emerald)' : 'var(--color-surface)'"
                        :stroke="'var(--color-emerald)'" stroke-width="2" class="marker" />
                </g>
            </svg>

            <!-- Пустой стейт -->
            <div v-else class="chart-empty">
                Нет данных за последние 6 месяцев
            </div>

            <!-- Тултип -->
            <Transition name="tooltip">
                <div v-if="hoveredIndex !== null && points[hoveredIndex]" class="chart-tooltip" :style="tooltipStyle">
                    <span class="tooltip-month">{{ months[hoveredIndex] }}</span>
                    <span class="tooltip-value">{{ formatCurrency(revenues[hoveredIndex]) }}</span>
                </div>
            </Transition>
        </div>

        <!-- Метки оси X -->
        <div class="x-axis">
            <span v-for="m in months" :key="m" class="x-tick">{{ m }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { PaymentResponse } from '../../types/payment';

const props = defineProps<{ payments: PaymentResponse[] }>();

/* ---- Размеры SVG (логические пиксели) ---- */
const SVG_W = 600;
const SVG_H = 200;
const PAD_X = 24; // отступ слева/справа от первой/последней точки
const PAD_T = 16; // отступ сверху
const PAD_B = 8;  // отступ снизу

/* ---- Данные ---- */
const months = computed<string[]>(() => {
    const result: string[] = [];
    const now = new Date();
    for (let i = 5; i >= 0; i--) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        result.push(d.toLocaleDateString('ru-RU', { month: 'short' }));
    }
    return result;
});

const revenues = computed<number[]>(() => {
    const now = new Date();
    return Array.from({ length: 6 }, (_, idx) => {
        const i = 5 - idx;
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const m = d.getMonth();
        const y = d.getFullYear();
        return props.payments
            .filter(p => {
                if (p.status !== 'paid' || !p.paid_at) return false;
                const pd = new Date(p.paid_at);
                return pd.getMonth() === m && pd.getFullYear() === y;
            })
            .reduce((sum, p) => sum + parseFloat(p.amount), 0);
    });
});

/* ---- Масштаб Y ---- */
const maxVal = computed(() => Math.max(...revenues.value, 1));

const yTicks = computed<number[]>(() => {
    const top = Math.ceil(maxVal.value / 1000) * 1000 || 10000;
    const step = top / 4;
    return [top, top - step, top - step * 2, step];
});

const yPos = (val: number) => {
    const top = yTicks.value[0];
    const ratio = 1 - val / top;
    return PAD_T + ratio * (SVG_H - PAD_T - PAD_B);
};

/* ---- Координаты точек ---- */
const points = computed(() =>
    revenues.value.map((rev, i) => {
        const x = PAD_X + (i / (revenues.value.length - 1)) * (SVG_W - PAD_X * 2);
        const y = yPos(rev);
        return { x, y };
    })
);

const polylinePoints = computed(() =>
    points.value.map(p => `${p.x},${p.y}`).join(' ')
);

const areaPath = computed(() => {
    if (!points.value.length) return '';
    const first = points.value[0];
    const last = points.value[points.value.length - 1];
    const line = points.value.map(p => `${p.x},${p.y}`).join(' L ');
    return `M ${first.x},${SVG_H} L ${line} L ${last.x},${SVG_H} Z`;
});

/* ---- Тултип ---- */
const hoveredIndex = ref<number | null>(null);

const tooltipStyle = computed(() => {
    if (hoveredIndex.value === null) return {};
    const p = points.value[hoveredIndex.value];
    const pctX = (p.x / SVG_W) * 100;
    return {
        left: `clamp(0px, calc(${pctX}% - 60px), calc(100% - 130px))`,
        top: '-52px',
    };
});

/* ---- Форматирование ---- */
const formatCurrency = (v: number) =>
    new Intl.NumberFormat('ru-RU', {
        style: 'currency', currency: 'RUB', minimumFractionDigits: 0,
    }).format(v);

const formatTick = (v: number) => {
    if (v >= 1_000_000) return (v / 1_000_000).toFixed(1) + 'M';
    if (v >= 1_000) return (v / 1_000).toFixed(0) + 'K';
    return String(v);
};

const chartAreaRef = ref<HTMLElement | null>(null);
</script>

<style scoped>
.chart-wrap {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    position: relative;
    padding-left: 36px;
    /* место под метки Y */
}

/* ---- Ось Y ---- */
.y-axis {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 28px;
    /* высота x-axis */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-bottom: var(--space-2);
}

.y-tick {
    font-size: 10px;
    font-weight: 500;
    color: var(--color-dark-35);
    font-variant-numeric: tabular-nums;
    line-height: 1;
}

/* ---- SVG-область ---- */
.chart-area {
    position: relative;
    flex: 1;
    min-height: 180px;
}

.chart-svg {
    width: 100%;
    height: 100%;
    min-height: 180px;
    overflow: visible;
}

.hover-zone {
    cursor: crosshair;
}

.marker {
    transition: fill 120ms ease;
}

/* ---- Ось X ---- */
.x-axis {
    display: flex;
    justify-content: space-between;
    padding: 0 4px;
}

.x-tick {
    font-size: 10px;
    font-weight: 500;
    color: var(--color-dark-35);
    text-align: center;
    flex: 1;
}

/* ---- Тултип ---- */
.chart-tooltip {
    position: absolute;
    background: var(--color-dark);
    color: var(--color-bg);
    border-radius: var(--radius-md);
    padding: var(--space-2) var(--space-3);
    font-size: var(--text-xs);
    pointer-events: none;
    white-space: nowrap;
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 120px;
}

.tooltip-month {
    color: rgba(251, 249, 244, 0.55);
    font-weight: 500;
}

.tooltip-value {
    font-size: var(--text-sm);
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}

.tooltip-enter-active,
.tooltip-leave-active {
    transition: opacity 120ms ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
    opacity: 0;
}

/* ---- Пустой стейт ---- */
.chart-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 180px;
    font-size: var(--text-sm);
    color: var(--color-dark-35);
}
</style>