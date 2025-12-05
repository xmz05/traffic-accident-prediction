<template>
  <div class="card">
    <h2>Параметры участка</h2>

    <form @submit.prevent="submit">
      <div class="field-group">
        <label>Участок дороги (описание)</label>
        <input
          v-model="form.road_segment"
          type="text"
          placeholder="Например, ТТК, съезд к Ленинградскому проспекту"
        />
      </div>

      <div class="field-row">
        <div class="field-group">
          <label>Широта</label>
          <input v-model.number="form.latitude" type="number" step="0.000001" placeholder="55.7558" />
        </div>
        <div class="field-group">
          <label>Долгота</label>
          <input v-model.number="form.longitude" type="number" step="0.000001" placeholder="37.6176" />
        </div>
      </div>

      <div class="field-group">
        <label>Дата и время (МСК)</label>
        <input v-model="form.datetime" type="datetime-local" />
      </div>

      <div class="field-row">
        <div class="field-group">
          <label>Погода</label>
          <select v-model="form.weather">
            <option value="clear">Ясно</option>
            <option value="rain">Дождь</option>
            <option value="snow">Снег</option>
            <option value="fog">Туман</option>
            <option value="ice">Гололёд</option>
          </select>
        </div>
        <div class="field-group">
          <label>Плотность трафика</label>
          <input
            v-model.number="form.traffic_density"
            type="range"
            min="0"
            max="1"
            step="0.01"
          />
          <div class="range-label">
            {{ (form.traffic_density * 100).toFixed(0) }} %
          </div>
        </div>
      </div>

      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? "Расчёт..." : "Рассчитать риск ДТП" }}
      </button>
    </form>

    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-if="result" class="result">
      <h3>Результат прогноза</h3>
      <p class="probability">
        Вероятность ДТП:
        <strong>{{ result.probability_percent }}%</strong>
      </p>
      <p class="cause">
        Вероятная причина: <strong>{{ result.cause }}</strong>
      </p>
      <p class="jam">
        Ожидаемый затор: <strong>{{ result.jam_level }}</strong>
      </p>
      <p class="jam-desc">
        {{ result.jam_description }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const form = ref({
  road_segment: "",
  latitude: 55.7558,
  longitude: 37.6176,
  datetime: "",
  weather: "clear",
  traffic_density: 0.5
});

const loading = ref(false);
const error = ref("");
const result = ref(null);

async function submit() {
  loading.value = true;
  error.value = "";
  result.value = null;

  try {
    const payload = {
      ...form.value,
      traffic_density: Number(form.value.traffic_density),
      datetime: form.value.datetime
        ? new Date(form.value.datetime).toISOString()
        : null
    };

    const response = await fetch("/api/predict/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || "Ошибка запроса к серверу");
    }

    const data = await response.json();
    result.value = data;
  } catch (e) {
    error.value = e.message || "Неизвестная ошибка";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.card {
  width: 100%;
  max-width: 720px;
  background: #020617;
  border-radius: 16px;
  padding: 24px 28px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid #1e293b;
}

h2 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 22px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.field-row .field-group {
  flex: 1;
  min-width: 180px;
}

label {
  font-size: 14px;
  color: #9ca3af;
}

input,
select {
  background: #020617;
  border-radius: 8px;
  border: 1px solid #1f2937;
  padding: 8px 10px;
  font-size: 14px;
  color: #e5e7eb;
  outline: none;
}

input:focus,
select:focus {
  border-color: #3b82f6;
}

input[type="range"] {
  padding: 0;
}

.range-label {
  font-size: 13px;
  color: #9ca3af;
}

.btn {
  margin-top: 8px;
  padding: 10px 16px;
  border-radius: 999px;
  border: none;
  background: linear-gradient(135deg, #3b82f6, #22c55e);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.08s ease, box-shadow 0.08s ease;
  align-self: flex-start;
}

.btn:disabled {
  opacity: 0.6;
  cursor: default;
  box-shadow: none;
  transform: none;
}

.btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 25px rgba(37, 99, 235, 0.35);
}

.alert {
  margin-top: 16px;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
}

.alert-error {
  background: rgba(248, 113, 113, 0.1);
  border: 1px solid #f87171;
  color: #fecaca;
}

.result {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px dashed #1f2937;
}

.result h3 {
  margin-top: 0;
  margin-bottom: 12px;
}

.probability strong {
  font-size: 20px;
}

.cause,
.jam,
.jam-desc {
  margin: 4px 0;
}
</style>
