<template>
  <div class="modal-overlay" v-if="ordem" @click.self="$emit('close')">
    <div class="modal" style="max-width: 560px">
      <div class="modal-header">
        <div>
          <h2>Diagnóstico</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px">
            OS #{{ ordem.id }}
          </p>
        </div>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div v-if="ordem.diagnostico">
          <div class="detail-grid" style="margin-bottom: 14px">
            <div class="detail-item">
              <div class="detail-label">Data</div>
              <div class="detail-value">{{ ordem.diagnostico.data || '—' }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Horas Estimadas</div>
              <div class="detail-value">{{ horasToTime(ordem.diagnostico.horas_estimadas) }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Orçamento Estimado</div>
              <div class="detail-value" style="color: var(--primary)">
                €{{ Number(ordem.diagnostico.orcamento_estimado || 0).toFixed(2) }}
              </div>
            </div>
          </div>
          <div class="detail-block">
            <div class="detail-label">Descrição</div>
            <div class="detail-text diag">{{ ordem.diagnostico.descricao }}</div>
          </div>
          <div class="detail-block" style="margin-top: 12px" v-if="ordem.diagnostico.pecas?.length > 0">
            <div class="detail-label" style="margin-bottom: 8px">Peças Previstas</div>
            <table class="view-table">
              <thead>
                <tr>
                  <th>ID Peça</th>
                  <th style="text-align: right">Qtd.</th>
                  <th style="text-align: right">Preço Unit.</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in ordem.diagnostico.pecas" :key="p.id_peca">
                  <td>#{{ p.id_peca }}</td>
                  <td style="text-align: right">{{ p.quantidade }}</td>
                  <td style="text-align: right">€{{ Number(p.preco_unitario || 0).toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state-detail" style="margin-top: 12px">
            <p>Nenhuma peça prevista no diagnóstico.</p>
          </div>
        </div>
        <div v-else class="empty-state-detail">
          <p><TriangleAlert :size="18" /> Sem diagnóstico registado para esta ordem.</p>
        </div>
        <div style="display: flex; justify-content: flex-end; margin-top: 16px">
          <button class="btn btn-secondary" @click="$emit('close')">Fechar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { TriangleAlert } from "@lucide/vue"
defineProps({
  ordem: { type: Object, default: null },
});

defineEmits(["close"]);

function horasToTime(horas) {
  if (!horas && horas !== 0) return "—";
  const h = Math.floor(Number(horas));
  const m = Math.round((Number(horas) - h) * 60);
  return m > 0 ? `${h}h ${m.toString().padStart(2, "0")}m` : `${h}h`;
}
</script>

<style scoped>
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
.view-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}
.view-table th {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  padding: 4px 8px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}
.view-table td {
  padding: 5px 8px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}
.view-table tbody tr:last-child td {
  border-bottom: none;
}
</style>
