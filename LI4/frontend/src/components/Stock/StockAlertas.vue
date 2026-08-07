<template>
  <div class="alertas-bloco">
    <div class="alertas-titulo"><TriangleAlert :size="18" /> Peças abaixo do stock mínimo ({{ alertasPecas.length }})</div>
    <div class="alertas-lista">
      <div v-for="p in alertasPecas" :key="p.id" class="alerta-item">
        <span class="alerta-nome">{{ p.nome }}</span>
        <span class="alerta-stock">
          Stock: <strong style="color: var(--danger)">{{ p.stockDisponivel }}</strong>
          / mínimo: {{ p.stockMinimo }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>

import { TriangleAlert } from "@lucide/vue"
defineProps({
  alertasPecas: Array,
})
</script>

<style scoped>
.alertas-bloco {
  margin-bottom: 20px;
  border: 1px solid #fecdd3;
  border-left: 4px solid var(--danger);
  border-radius: var(--radius-sm);
  background: #fff1f2;
  padding: 12px 16px;
}
.alertas-titulo {
  font-weight: 700;
  font-size: 0.875rem;
  color: #be123c;
  margin-bottom: 8px;
}
.alertas-lista {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.alerta-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  padding: 4px 0;
  border-bottom: 1px solid #fecdd3;
}
.alerta-item:last-child {
  border-bottom: none;
}
.alerta-nome {
  font-weight: 600;
  color: var(--text);
}
.alerta-stock {
  color: var(--text-muted);
}
</style>
