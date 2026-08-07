<template>
  <div class="card">
    <div class="section-header">
      <div>
        <div class="chart-title">Alertas de Stock</div>
        <div class="chart-sub">Peças abaixo do mínimo</div>
      </div>
      <router-link to="/stock" class="btn btn-secondary" style="font-size: 0.8rem; padding: 6px 12px">
        Ver stock <ArrowRight :size="14" />
      </router-link>
    </div>
    <div class="stock-list">
      <div v-for="peca in pecas" :key="peca.id" class="stock-item">
        <div class="stock-info">
          <div class="stock-nome">{{ peca.nome }}</div>
          <div class="stock-codigo">{{ peca.codigo }}</div>
        </div>
        <div class="stock-badge-wrap">
          <span class="badge" :class="peca.estado === 'Crítico' ? 'badge-danger' : 'badge-warning'">
            {{ peca.stockDisponivel }} unidades
          </span>
          <div class="stock-min">Mín: {{ peca.stockMinimo }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ArrowRight } from "@lucide/vue"
defineProps({ pecas: Array })
</script>

<style scoped>
.chart-title { font-weight: 700; font-size: 0.95rem; }
.chart-sub { font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; }
.section-header { display: flex; align-items: flex-start; justify-content: space-between; padding: 18px 20px 12px; border-bottom: 1px solid var(--border); }
.stock-list { padding: 8px 0; }
.stock-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 20px; border-bottom: 1px solid var(--border); }
.stock-item:last-child { border-bottom: none; }
.stock-nome { font-weight: 600; font-size: 0.875rem; }
.stock-codigo { font-size: 0.72rem; color: var(--text-light); font-family: "DM Mono", monospace; margin-top: 2px; }
.stock-badge-wrap { text-align: right; }
.stock-min { font-size: 0.7rem; color: var(--text-light); margin-top: 3px; }
</style>
