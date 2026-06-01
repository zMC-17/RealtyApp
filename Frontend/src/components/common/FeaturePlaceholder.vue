<script setup lang="ts">
defineProps<{
  title: string;
  description: string;
  bullets?: string[];
}>();
</script>

<template>
  <div class="placeholder-page">
    <div class="placeholder-card">
      <p class="eyebrow">Frontend scaffold</p>
      <h1>{{ title }}</h1>
      <p class="description">{{ description }}</p>

      <ul v-if="bullets?.length" class="bullet-list">
        <li v-for="bullet in bullets" :key="bullet">{{ bullet }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.placeholder-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 2rem;
  background:
    radial-gradient(circle at top left, rgba(168, 85, 247, 0.18), transparent 32%),
    radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.16), transparent 30%),
    linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}

.placeholder-card {
  width: min(760px, 100%);
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 24px;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(12px);
  box-shadow: 0 24px 80px rgba(15, 23, 42, 0.12);
}

.eyebrow {
  margin: 0 0 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.78rem;
  color: #6b7280;
}

h1 {
  margin: 0;
  font-size: clamp(1.8rem, 3vw, 2.6rem);
  line-height: 1.1;
  color: #0f172a;
}

.description {
  margin: 1rem 0 0;
  font-size: 1rem;
  line-height: 1.7;
  color: #334155;
}

.bullet-list {
  margin: 1.25rem 0 0;
  padding-left: 1.2rem;
  color: #0f172a;
}

.bullet-list li {
  margin-top: 0.6rem;
  line-height: 1.55;
}
</style>