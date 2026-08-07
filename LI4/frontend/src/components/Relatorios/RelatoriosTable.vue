<template>
  <div class="card">
    <div class="table-header">
      <h3>Relatórios</h3>
    </div>

    <div v-if="loading" class="empty-row">A carregar...</div>
    <div v-else-if="error" class="empty-row" style="color: var(--danger)">{{ error }}</div>

    <div v-else class="table-wrap">
      <table class="faturas-table">
        <thead>
          <tr>
            <th>Nome do Ficheiro</th>
            <th>Tipo</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in filtered" :key="r.id">
            <td class="fatura-num">{{ r.nome_arquivo }}</td>
            <td>
              <span class="badge" :class="tipoBadge(r.tipo_relatorio)">
                {{ r.tipo_relatorio }}
              </span>
            </td>
            <td>
              <div class="acoes">
                <button
                  class="acao-btn"
                  @click="$emit('view', r)"
                  title="Ver"
                >
                  <Eye :size="18" />
                </button>
                <button
                  class="acao-btn"
                  @click="download(r)"
                  title="Descarregar"
                >
                  <Download :size="18" />
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filtered.length === 0">
            <td colspan="3" class="empty-row">Nenhum relatório encontrado.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>

import { Download } from "@lucide/vue"
import { Eye } from "@lucide/vue"
import { useRelatorios } from "@/composables/useRelatorios";
import { tipoBadge } from "@/helpers";

const { downloadRelatorioPDF } = useRelatorios();

defineProps({
  relatorios: { type: Array, required: true },
  filtered: { type: Array, required: true },
  loading: { type: Boolean, required: true },
  error: { type: String, default: null },
})

defineEmits(['view'])

function download(r) {
  downloadRelatorioPDF(r.id, r.nome_arquivo)
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
