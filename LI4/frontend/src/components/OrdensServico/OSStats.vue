<template>
  <div class="stats-row" style="margin-bottom: 20px">
    <div class="stat-card">
      <div class="label">Em Aberto</div>
      <div class="value">{{ emAberto }}</div>
      <div class="icon"><AlarmClock :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Concluídas</div>
      <div class="value" style="color: var(--success)">{{ concluidas }}</div>
      <div class="icon"><CheckCircle :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Em Reparação</div>
      <div class="value" style="color: var(--danger)">{{ emReparacao }}</div>
      <div class="icon"><Wrench :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Aguarda Faturação</div>
      <div class="value" style="color: var(--warning)">{{ aguardaFaturacao }}</div>
      <div class="icon"><Package :size="18" /></div>
    </div>
  </div>
</template>

<script setup>

import { AlarmClock } from "@lucide/vue"
import { CheckCircle } from "@lucide/vue"
import { Package } from "@lucide/vue"
import { Wrench } from "@lucide/vue"
defineProps({
  emAberto: { type: Number, default: 0 },
  concluidas: { type: Number, default: 0 },
  emReparacao: { type: Number, default: 0 },
  aguardaFaturacao: { type: Number, default: 0 },
});
</script>

<style scoped>
.stat-card {
  background: white;
  border-radius: var(--radius);
  padding: 16px 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  position: relative;
}
.stat-card .label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.stat-card .value {
  font-size: 1.8rem;
  font-weight: 800;
  margin-top: 4px;
}
.stat-card .icon {
  position: absolute;
  top: 12px;
  right: 14px;
  font-size: 1.5rem;
  opacity: 0.25;
}
</style>
