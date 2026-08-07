<template>
  <div class="stats-row" style="margin-bottom: 20px">
    <div class="stat-card">
      <div class="label">Total de Faturas</div>
      <div class="value">{{ totalFaturas }}</div>
      <div class="icon"><FileText :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Receita Recebida</div>
      <div class="value" style="color: var(--success); font-size: 1.3rem">
        €{{ receitaRecebida.toFixed(2) }}
      </div>
      <div class="icon"><CheckCircle :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Por Pagar</div>
      <div class="value" style="color: var(--warning); font-size: 1.3rem">
        {{ porPagar }}
      </div>
      <div class="icon"><Hourglass :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Vencidas</div>
      <div class="value" style="color: var(--danger)">{{ vencidas }}</div>
      <div class="icon"><TriangleAlert :size="18" /></div>
    </div>
  </div>
</template>

<script setup>

import { CheckCircle } from "@lucide/vue"
import { FileText } from "@lucide/vue"
import { Hourglass } from "@lucide/vue"
import { TriangleAlert } from "@lucide/vue"
defineProps({
  totalFaturas: Number,
  receitaRecebida: Number,
  porPagar: Number,
  vencidas: Number,
})
</script>

<style scoped>
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
@media (max-width: 900px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 520px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.stat-card .label {
  font-size: 0.78rem;
  color: var(--text-muted);
  font-weight: 500;
}
.stat-card .value {
  font-size: 1.6rem;
  font-weight: 700;
  line-height: 1;
}
.stat-card .icon {
  font-size: 1.2rem;
  align-self: flex-end;
  margin-top: -4px;
}
</style>
