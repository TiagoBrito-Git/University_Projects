<template>
  <div class="card">
    <div class="section-header">
      <div>
        <div class="chart-title">Ordens de Serviço Recentes</div>
        <div class="chart-sub">Últimas {{ ordens.length }} ordens</div>
      </div>
      <router-link to="/ordens-servico" class="btn btn-secondary" style="font-size: 0.8rem; padding: 6px 12px">
        Ver todas <ArrowRight :size="14" />
      </router-link>
    </div>
    <div class="ordem-list">
      <div v-for="ordem in ordens" :key="ordem.id" class="ordem-item">
        <div class="ordem-icon" :style="{ background: estadoColor(ordem.estado) }">
          <component :is="estadoIcone(ordem.estado)" :size="18" />
        </div>
        <div class="ordem-info">
          <div class="ordem-titulo">{{ ordem.titulo }}</div>
          <div class="ordem-meta">
            {{ ordem.clienteNome || '—' }} · {{ ordem.equipamentoNome || '—' }}
          </div>
          <div class="ordem-tags">
            <span class="badge" :class="estadoBadge(ordem.estado)">{{ ordem.estado }}</span>
          </div>
        </div>
        <div class="ordem-date">{{ ordem.abertura }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ArrowRight, Hourglass, Search, Wrench, Package, CheckCircle, DollarSign, Lock, XCircle } from "@lucide/vue"
import { estadoBadge, estadoColor } from "@/helpers"
defineProps({ ordens: Array })

function estadoIcone(estado) {
  const map = { "Aguarda Diagnóstico": Hourglass, "Aguarda Resposta": Search, "Em Reparação": Wrench, "Aguarda Faturação": Package, Concluído: CheckCircle, Faturada: DollarSign, Encerrada: Lock, Cancelada: XCircle }
  return map[estado]
}
</script>

<style scoped>
.chart-title { font-weight: 700; font-size: 0.95rem; }
.chart-sub { font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; }
.section-header { display: flex; align-items: flex-start; justify-content: space-between; padding: 18px 20px 12px; border-bottom: 1px solid var(--border); }
.ordem-list { padding: 8px 0; }
.ordem-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 20px; border-bottom: 1px solid var(--border); transition: background var(--transition); }
.ordem-item:last-child { border-bottom: none; }
.ordem-item:hover { background: var(--bg); }
.ordem-icon { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.ordem-info { flex: 1; min-width: 0; }
.ordem-titulo { font-weight: 600; font-size: 0.875rem; }
.ordem-meta { font-size: 0.75rem; color: var(--text-muted); margin: 2px 0 5px; }
.ordem-date { font-size: 0.72rem; color: var(--text-light); white-space: nowrap; }
</style>
