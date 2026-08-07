<template>
  <div class="card">
    <div class="table-header">
      <h3>Faturas</h3>
    </div>
    <div class="table-wrap">
      <table class="faturas-table">
        <thead>
          <tr>
            <th>Número</th>
            <th>Cliente</th>
            <th>Data Emissão</th>
            <th>Vencimento</th>
            <th>Estado</th>
            <th>Total</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="fatura in filtered" :key="fatura.id">
            <td class="fatura-num">{{ fatura.numero }}</td>
            <td>{{ fatura.nomeCliente || '—' }}</td>
            <td>{{ fatura.emissao }}</td>
            <td :class="{ vencida: isVencida(fatura) }">
              {{ fatura.vencimento }}
            </td>
            <td>
              <span class="badge" :class="estadoBadge(fatura.estado)">{{
                fatura.estado
              }}</span>
            </td>
            <td class="total-cell">€{{ fatura.total.toFixed(2) }}</td>
            <td>
              <div class="acoes">
                <button
                  class="acao-btn"
                  @click="$emit('view', fatura)"
                  title="Ver"
                >
                  <Eye :size="18" />
                </button>
                <button
                  class="acao-btn"
                  @click="download(fatura)"
                  title="Descarregar"
                >
                  <Download :size="18" />
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filtered.length === 0">
            <td colspan="7" class="empty-row">Nenhuma fatura encontrada.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>

import { Download } from "@lucide/vue"
import { Eye } from "@lucide/vue"
import { useFaturacao } from "@/composables/useFaturacao";
import { faturaBadge as estadoBadge, isVencida } from "@/helpers";

const { downloadFaturaPDF } = useFaturacao();

defineProps({
  filtered: Array,
})
defineEmits(['view'])

function download(fatura) {
  downloadFaturaPDF(fatura.id, fatura.numero)
}
</script>

<style scoped>
.table-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}
.table-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
}
.table-wrap {
  overflow-x: auto;
}
.faturas-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}
.faturas-table th {
  text-align: left;
  padding: 10px 16px;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}
.faturas-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
}
.faturas-table tr:last-child td {
  border-bottom: none;
}
.faturas-table tbody tr:hover {
  background: var(--bg);
}
.fatura-num {
  font-family: "DM Mono", monospace;
  font-weight: 600;
  color: var(--primary);
}
.total-cell {
  font-weight: 700;
}
.vencida {
  color: var(--danger) !important;
  font-weight: 600;
}
.acoes {
  display: flex;
  gap: 4px;
}
.acao-btn {
  padding: 4px 8px;
  border-radius: 4px;
  transition: background var(--transition);
}
.acao-btn:hover {
  background: var(--bg);
}
.empty-row {
  text-align: center;
  color: var(--text-muted);
  padding: 32px;
}
</style>
