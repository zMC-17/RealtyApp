<!-- components/dashboard/RevenueChart.vue -->
<template>
    <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import type { PaymentResponse } from '../../types/payment';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, Filler);

const props = defineProps<{
    payments: PaymentResponse[];
}>();

const chartData = computed(() => {
    // Последние 6 месяцев
    const months: string[] = [];
    const revenue: number[] = [];
    const now = new Date();

    for (let i = 5; i >= 0; i--) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const monthLabel = d.toLocaleDateString('ru-RU', { month: 'short' });
        const year = d.getFullYear();
        const month = d.getMonth();

        const monthRevenue = props.payments
            .filter(p => {
                if (p.status !== 'paid' || !p.paid_at) return false;
                const paidDate = new Date(p.paid_at);
                return paidDate.getMonth() === month && paidDate.getFullYear() === year;
            })
            .reduce((sum, p) => sum + parseFloat(p.amount), 0);

        months.push(`${monthLabel} ${year}`);
        revenue.push(monthRevenue);
    }

    return {
        labels: months,
        datasets: [
            {
                label: 'Выручка (₽)',
                data: revenue,
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                borderColor: '#667eea',
                borderWidth: 1,
                borderRadius: 6,
            },
        ],
    };
});

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
            callbacks: {
                label: (context: any) => {
                    let value = context.parsed.y;
                    return new Intl.NumberFormat('ru-RU', {
                        style: 'currency',
                        currency: 'RUB',
                        minimumFractionDigits: 0,
                    }).format(value);
                },
            },
        },
    },
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                callback: (value: any) => {
                    if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M ₽';
                    if (value >= 1000) return (value / 1000).toFixed(0) + 'K ₽';
                    return value + ' ₽';
                },
            },
        },
    },
};
</script>