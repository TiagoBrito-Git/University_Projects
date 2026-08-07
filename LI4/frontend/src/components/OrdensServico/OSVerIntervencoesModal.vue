<template>
  <div class="modal-overlay" v-if="ordem" @click.self="$emit('close')">
    <div class="modal" style="max-width: 640px">
      <div class="modal-header">
        <div>
          <h2>Intervenções</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px">
            OS #{{ ordem.id }} · {{ ordem.intervencoes?.length || 0 }} intervenção(ões)
          </p>
        </div>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div v-if="ordem.intervencoes?.length > 0">
          <div
            v-for="(inv, idx) in ordem.intervencoes"
            :key="inv.id"
            class="inv-card"
          >
            <div class="inv-header">
              <span class="inv-num">Intervenção {{ idx + 1 }}</span>
              <span class="inv-data">{{ inv.data }}</span>
              <span class="inv-custo">€{{ Number(inv.custo || 0).toFixed(2) }}</span>
            </div>
            <div class="detail-text" style="margin-top: 6px">{{ inv.descricao }}</div>
            <div class="inv-meta" style="margin-top: 6px">
              <span><Clock :size="18" /> {{ horasToTime(inv.horas) }} trabalhadas</span>
            </div>
            <div v-if="inv.pecas?.length > 0" style="margin-top: 8px">
              <div class="detail-label" style="margin-bottom: 4px">Peças usadas</div>
              <table class="view-table">
                <thead>
                  <tr>
                    <th>ID Peça</th>
                    <th style="text-align: right">Qtd.</th>
                    <th style="text-align: right">Preço Unit.</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="p in inv.pecas" :key="p.id_peca">
                    <td>#{{ p.id_peca }}</td>
                    <td style="text-align: right">{{ p.quantidade }}</td>
                    <td style="text-align: right">€{{ Number(p.preco_unitario || 0).toFixed(2) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="inv-total">
            Total gasto:
            <strong style="color: var(--primary)">
              €{{ ordem.intervencoes.reduce((s, i) => s + (i.custo || 0), 0).toFixed(2) }}
            </strong>
          </div>
        </div>
        <div v-else class="empty-state-detail">
          <p><Wrench :size="18" /> Nenhuma intervenção registada.</p>
        </div>
        <div style="display: flex; justify-content: flex-end; margin-top: 16px">
          <button class="btn btn-secondary" @click="$emit('close')">Fechar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { Clock } from "@lucide/vue"
import { Wrench } from "@lucide/vue"
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
.inv-card {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  margin-bottom: 10px;
}
.inv-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 2px;
}
.inv-num {
  font-weight: 700;
  font-size: 0.875rem;
  flex: 1;
}
.inv-data {
  font-size: 0.78rem;
  color: var(--text-muted);
}
.inv-custo {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--primary);
}
.inv-meta {
  font-size: 0.78rem;
  color: var(--text-muted);
}
.inv-total {
  margin-top: 8px;
  padding: 10px 14px;
  background: var(--primary-light, #eff6ff);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  text-align: right;
}
.detail-label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 3px;
}
.detail-text {
  background: var(--bg);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 0.875rem;
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
