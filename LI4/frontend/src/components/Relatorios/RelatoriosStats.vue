<template>
  <div class="stats-row" style="margin-bottom: 20px">
    <div class="stat-card">
      <div class="label">Total de Relatórios</div>
      <div class="value">{{ total }}</div>
      <div class="icon"><BarChart3 :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Económicos</div>
      <div class="value" style="color: var(--success)">
        {{ economicos }}
      </div>
      <div class="icon"><DollarSign :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Stock</div>
      <div class="value" style="color: var(--warning)">
        {{ stock }}
      </div>
      <div class="icon"><Package :size="18" /></div>
    </div>
    <div class="stat-card">
      <div class="label">Performance</div>
      <div class="value" style="color: var(--danger)">
        {{ performance }}
      </div>
      <div class="icon"><Zap :size="18" /></div>
    </div>
  </div>
</template>

<script setup>

import { BarChart3 } from "@lucide/vue"
import { DollarSign } from "@lucide/vue"
import { Package } from "@lucide/vue"
import { Zap } from "@lucide/vue"
import { computed } from "vue";

const props = defineProps({
  relatorios: { type: Array, required: true },
})

const total = computed(() => props.relatorios.length)
const economicos = computed(() => props.relatorios.filter((r) => r.tipo_relatorio === "Económico").length)
const stock = computed(() => props.relatorios.filter((r) => r.tipo_relatorio === "Stock").length)
const performance = computed(() => props.relatorios.filter((r) => r.tipo_relatorio === "Performance").length)
</script>

<style scoped>
</style>
