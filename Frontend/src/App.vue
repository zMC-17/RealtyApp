<script setup lang="ts">
/**
 * Главный компонент приложения RealtyApp
 *
 * Корневой компонент приложения, который:
 * - Подключает Vue Router для навигации
 * - Выводит текущий маршрут через <router-view>
 * - Обеспечивает единую точку входа для всех страниц
 */
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f5f5;
}

#app {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>
