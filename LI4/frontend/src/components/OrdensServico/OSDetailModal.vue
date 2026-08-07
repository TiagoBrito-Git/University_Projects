<template>
  <div class="modal-overlay" v-if="ordem" @click.self="$emit('close')">
    <div class="modal" style="max-width: 560px">
      <div class="modal-header">
        <h2>OS #{{ ordem.id }}</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="detail-badges" style="margin-bottom: 14px; display: flex; gap: 6px">
          <span class="badge" :class="estadoBadge(ordem.estado)">{{ ordem.estado }}</span>
        </div>
        <div class="detail-grid">
          <div class="detail-item">
            <div class="detail-label">Cliente</div>
            <div class="detail-value">{{ ordem.clienteNome }}</div>
            <div class="detail-sub">{{ ordem.clienteEmail }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">Equipamento</div>
            <div class="detail-value">{{ ordem.equipamentoNome }}</div>
            <div class="detail-sub">Nº Série: {{ ordem.numeroSerie }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">Técnico Responsável</div>
            <div class="detail-value tecnico-highlight">{{ ordem.tecnico }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">Data de Abertura</div>
            <div class="detail-value">{{ ordem.abertura }}</div>
          </div>
        </div>
        <div class="detail-block" style="margin-top: 14px">
          <div class="detail-label">Descrição do Problema</div>
          <div class="detail-text">{{ ordem.descricao }}</div>
        </div>

        <div class="detail-block" style="margin-top: 12px">
          <div class="detail-label">Diagnóstico</div>
          <div v-if="ordem.diagnostico" class="detail-text diag">
            {{ ordem.diagnostico.descricao }}
            <div style="margin-top: 6px; font-size: 0.8rem; color: var(--text-muted)">
              Tempo estimado: <strong>{{ horasToTime(ordem.diagnostico.horas_estimadas) }}</strong>
              &nbsp;·&nbsp; Orçamento: <strong>€{{ Number(ordem.diagnostico.orcamento_estimado).toFixed(2) }}</strong>
            </div>
          </div>
          <div v-else class="empty-state-detail">
            <p><TriangleAlert :size="18" /> Ainda não foi registado um diagnóstico para esta ordem.</p>
          </div>
        </div>

        <div class="detail-block" style="margin-top: 12px">
          <div class="detail-label">Intervenções</div>
          <div v-if="ordem.intervencoes?.length > 0" class="detail-text">
            {{ ordem.intervencoes.length }} intervenção(ões) registada(s).
            Custo total: <strong style="color: var(--primary)">
              €{{ ordem.intervencoes.reduce((s, i) => s + (i.custo || 0), 0).toFixed(2) }}
            </strong>
          </div>
          <div v-else class="empty-state-detail">
            <p><Wrench :size="18" /> Nenhuma intervenção registada até ao momento.</p>
          </div>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; margin-top: 16px">
          <button class="btn btn-secondary" @click="$emit('close')">Fechar</button>
          <button
            v-if="ordem.diagnostico"
            class="btn btn-secondary"
            @click="$emit('abrir-ver-diagnostico', ordem)"
          >
            <ClipboardList :size="18" /> Ver Diagnóstico
          </button>
          <button
            v-if="ordem.intervencoes?.length > 0"
            class="btn btn-secondary"
            @click="$emit('abrir-ver-intervencoes', ordem)"
          >
            <Settings :size="18" /> Ver Intervenções
          </button>
          <button
            v-if="ordem.estado === 'Aguarda Diagnóstico'"
            class="btn btn-purple"
            @click="$emit('abrir-diagnostico', ordem)"
          >
            <Search :size="18" /> Registar Diagnóstico
          </button>
          <button
            v-if="ordem.estado === 'Aguarda Resposta'"
            class="btn btn-purple"
            @click="$emit('abrir-resposta', ordem)"
          >
            <MessageSquare :size="18" /> Registar Resposta
          </button>
          <button
            v-if="ordem.estado === 'Em Reparação'"
            class="btn btn-purple"
            @click="$emit('abrir-intervencao', ordem)"
          >
            <Wrench :size="18" /> Registar Intervenção
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ClipboardList } from "@lucide/vue"
import { MessageSquare } from "@lucide/vue"
import { Search } from "@lucide/vue"
import { Settings } from "@lucide/vue"
import { TriangleAlert } from "@lucide/vue"
import { Wrench } from "@lucide/vue"
import { estadoBadge } from "@/helpers"
defineProps({
  ordem: { type: Object, default: null },
});

defineEmits(["close", "abrir-diagnostico", "abrir-resposta", "abrir-intervencao", "abrir-ver-diagnostico", "abrir-ver-intervencoes"]);

function horasToTime(horas) {
  if (!horas && horas !== 0) return "—";
  const h = Math.floor(Number(horas));
  const m = Math.round((Number(horas) - h) * 60);
  return m > 0 ? `${h}h ${m.toString().padStart(2, "0")}m` : `${h}h`;
}
</script>

<style scoped>
.detail-badges {
  display: flex;
  gap: 6px;
}
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.detail-label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 3px;
}
.detail-value {
  font-weight: 600;
  font-size: 0.9rem;
}
.detail-sub {
  font-size: 0.75rem;
  color: var(--text-muted);
}
.tecnico-highlight {
  background: var(--primary-light);
  color: var(--primary);
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
}
.detail-block {
  margin-top: 12px;
}
.detail-text {
  background: var(--bg);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 0.875rem;
}
.diag {
  border-left: 3px solid var(--primary);
}
.empty-state-detail {
  background: var(--bg);
  border-radius: var(--radius-sm);
  padding: 14px;
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}
</style>
