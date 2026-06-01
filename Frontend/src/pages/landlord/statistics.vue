<script setup lang="ts">
import FeaturePlaceholder from '../../components/common/FeaturePlaceholder.vue';
</script>

<template>
  <FeaturePlaceholder
    title="Статистика владельца"
    description="Mock-статистика удалена. Этот экран будет собирать данные из реальных договоров, платежей и объектов после подключения backend API."
    :bullets="[
      'Нужно показывать доход, число объектов и активные договоры.',
      'Данные должны считаться из реальных ответов backend, а не из локальных заглушек.',
      'Графики можно добавить только после стабилизации доменных списков.'
    ]"
  />
</template>
