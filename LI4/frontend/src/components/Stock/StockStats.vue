<template>
  <div class="stats-row" style="margin-bottom: 20px">
    <div class="stat-card">
      <div class="label">Itens no Stock</div>
      <div class="value">{{ totalItens }}</div>
      <div class="icon"><Package :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Alertas de Stock</div>
      <div class="value" style="color: var(--danger)">{{ alertas }}</div>
      <div class="icon"><TriangleAlert :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Valor Total</div>
      <div class="value" style="font-size: 1.3rem">
        €{{ valorTotal.toFixed(2) }}
      </div>
      <div class="icon"><BarChart3 :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Categorias</div>
      <div class="value">{{ categoriasCount }}</div>
      <div class="icon"><Tag :size="18" /></div>
    </div>
  </div>
</template>

<script setup>

import { BarChart3 } from "@lucide/vue"
import { Package } from "@lucide/vue"
import { Tag } from "@lucide/vue"
import { TriangleAlert } from "@lucide/vue"
defineProps({
  totalItens: Number,
  alertas: Number,
  valorTotal: Number,
  categoriasCount: Number,
})
</script>
