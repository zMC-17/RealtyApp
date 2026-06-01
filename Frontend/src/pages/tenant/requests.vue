<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Мои заявки"
    description="Mock-заявки удалены. Этот экран будет подключаться к GET /requests/tenant/me и POST /requests."
    :bullets="[
      'Арендатор должен создавать заявку по договору.',
      'Список должен подтягиваться из backend, а не из mock-фильтра.',
      'Здесь позже появятся статусы обработки заявки.'
    ]"
  />
</template>
