<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Мои платежи"
    description="Mock-платежи удалены. Этот экран будет подключаться к GET /payments/tenant/me и GET /payments/contracts/{contract_id}."
    :bullets="[
      'Нужны реальные статусы оплаты и даты.',
      'Сценарий оплаты должен работать поверх backend.',
      'Платежи лучше показывать вместе с договором.'
    ]"
  />
</template>
