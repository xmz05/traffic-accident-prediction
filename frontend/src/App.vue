<template>
  <div class="app">
    <header class="header">
      <h1>Прогноз аварийности на дорогах Москвы</h1>
      <p>Введите параметры участка дороги и времени, чтобы получить оценку риска ДТП.</p>
    </header>

    <main class="main">
      <PredictionForm />
    </main>
  </div>
</template>

<script setup>
import PredictionForm from "./components/PredictionForm.vue";
</script>

<style>
.app {
  min-height: 100vh;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #0f172a;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
}

.header {
  padding: 24px 32px;
  border-bottom: 1px solid #1f2937;
  background: radial-gradient(circle at top, #1e293b 0, #020617 55%);
}

.header h1 {
  margin: 0 0 8px;
  font-size: 28px;
}

.header p {
  margin: 0;
  color: #9ca3af;
}

.main {
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 32px 16px;
}
</style>
