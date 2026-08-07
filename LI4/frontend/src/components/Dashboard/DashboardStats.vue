<template>
  <div class="stats-row">
    <div class="stat-card">
      <div class="label">Ordens em Aberto</div>
      <div class="value">{{ ordensEmAberto }}</div>
      <div class="sub">Ordens ativas</div>
      <div class="icon"><ClipboardList :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Clientes Ativos</div>
      <div class="value">{{ clientesCount }}</div>
      <div class="sub">Total de {{ clientesCount }} clientes</div>
      <div class="icon"><Users :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Peças Baixo Stock</div>
      <div class="value" style="color: var(--danger)">{{ pecasBaixoStock }}</div>
      <div class="sub" style="color: var(--danger)">Requer atenção</div>
      <div class="icon"><TriangleAlert :size="18" /></div>
    </div>
  </div>
</template>

<script setup>

import { ClipboardList } from "@lucide/vue"
import { TriangleAlert } from "@lucide/vue"
import { Users } from "@lucide/vue"
defineProps({
  ordensEmAberto: Number,
  clientesCount: Number,
  pecasBaixoStock: Number,
})
</script>
