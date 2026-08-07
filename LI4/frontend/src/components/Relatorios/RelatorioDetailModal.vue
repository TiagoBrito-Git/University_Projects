<template>
  <div
    class="modal-overlay"
    v-if="relatorio"
    @click.self="$emit('close')"
  >
    <div class="modal" style="max-width: 480px">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 10px">
          <h2>{{ relatorio.nome_arquivo }}</h2>
          <span class="badge" :class="tipoBadge(relatorio.tipo_relatorio)">
            {{ relatorio.tipo_relatorio }}
          </span>
        </div>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="fatura-section">
          <div class="section-label">Ficheiro</div>
          <div class="cliente-block">
            <div class="cli-nome">{{ relatorio.nome_arquivo }}</div>
            <div class="cli-detail">Tipo: {{ relatorio.tipo_relatorio }}</div>
          </div>
        </div>

        <div style="display: flex; gap: 8px; margin-top: 20px">
          <button
            class="btn btn-primary"
            style="flex: 1; justify-content: center"
            @click="download"
          >
            <Download :size="18" /> Descarregar PDF
          </button>
          <button class="btn btn-secondary" @click="$emit('close')">
            Fechar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { Download } from "@lucide/vue"
import { useRelatorios } from "@/composables/useRelatorios";

const { downloadRelatorioPDF } = useRelatorios();

const props = defineProps({
  relatorio: { type: Object, default: null },
})

defineEmits(['close'])

function download() {
  downloadRelatorioPDF(props.relatorio.id, props.relatorio.nome_arquivo)
}

function tipoBadge(tipo) {
  const m = {
    Económico: "badge-success",
    Stock: "badge-info",
    Performance: "badge-warning",
  }
  return m[tipo] || "badge-gray"
}
</script>

<style scoped>
.fatura-section {
  margin-bottom: 16px;
}
.section-label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.cliente-block {
  background: var(--bg);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}
.cli-nome {
  font-weight: 700;
}
.cli-detail {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 2px;
}
</style>
