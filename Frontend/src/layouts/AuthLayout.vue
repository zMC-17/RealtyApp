<!-- src/layouts/AuthLayout.vue -->
<template>
  <div class="auth-layout">

    <!-- Многослойный фон -->
    <div class="auth-bg" aria-hidden="true">
      <!-- Базовый mesh-градиент -->
      <div class="bg-base"></div>
      <!-- Цветовые пятна -->
      <div class="bg-blob bg-blob--rose"></div>
      <div class="bg-blob bg-blob--lilac"></div>
      <div class="bg-blob bg-blob--peach"></div>
      <div class="bg-blob bg-blob--olive"></div>
      <!-- Шумовая текстура поверх -->
      <div class="bg-noise"></div>
    </div>

    <!-- Декоративный логотип в углу -->
    <div class="auth-wordmark">
      <span class="wordmark-mark">R</span>
      <span class="wordmark-text">Realty</span>
    </div>

    <!-- Контент (карточка формы) -->
    <div class="auth-content">
      <router-view />
    </div>

  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
/* ============ Обёртка ============ */
.auth-layout {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-4);
  overflow: hidden;
  isolation: isolate;
}

/* ============ Фоновые слои ============ */
.auth-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

/* Базовый тёплый кремовый */
.bg-base {
  position: absolute;
  inset: 0;
  background: #F2EDE3;
}

/* Цветовые пятна — крупные, насыщенные */
.bg-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

/* Роза — верхний правый угол, большое */
.bg-blob--rose {
  width: 70vw;
  height: 65vh;
  top: -20vh;
  right: -20vw;
  background: radial-gradient(circle at 40% 40%,
      rgba(196, 120, 138, 0.72) 0%,
      rgba(196, 120, 138, 0.35) 40%,
      transparent 70%);
}

/* Сиреневый — нижний левый, широкое */
.bg-blob--lilac {
  width: 65vw;
  height: 60vh;
  bottom: -15vh;
  left: -15vw;
  background: radial-gradient(circle at 60% 60%,
      rgba(155, 137, 180, 0.68) 0%,
      rgba(155, 137, 180, 0.30) 45%,
      transparent 70%);
}

/* Персик — нижний правый */
.bg-blob--peach {
  width: 45vw;
  height: 40vh;
  bottom: -5vh;
  right: 5vw;
  background: radial-gradient(circle at 50% 50%,
      rgba(196, 154, 120, 0.55) 0%,
      rgba(196, 154, 120, 0.20) 50%,
      transparent 70%);
}

/* Оливковый — верхний левый, небольшое */
.bg-blob--olive {
  width: 40vw;
  height: 35vh;
  top: 5vh;
  left: -5vw;
  background: radial-gradient(circle at 50% 50%,
      rgba(141, 169, 138, 0.45) 0%,
      rgba(141, 169, 138, 0.18) 50%,
      transparent 70%);
}

/* Очень тонкая шумовая текстура для «глубины» */
.bg-noise {
  position: absolute;
  inset: 0;
  opacity: 0.028;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size: 200px 200px;
  pointer-events: none;
}

/* ============ Логотип в углу ============ */
.auth-wordmark {
  position: absolute;
  top: var(--space-6);
  left: var(--space-8);
  z-index: 2;
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.wordmark-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: var(--color-emerald);
  color: #fff;
  font-size: var(--text-sm);
  font-weight: 800;
  border-radius: var(--radius-sm);
}

.wordmark-text {
  font-size: var(--text-md);
  font-weight: 700;
  color: var(--color-dark);
  letter-spacing: -0.02em;
}

/* ============ Контент ============ */
.auth-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 400px;
}
</style>