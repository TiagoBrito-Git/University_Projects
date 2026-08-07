<template>
  <div class="modal-overlay" v-if="fatura" @click.self="$emit('close')">
    <div class="modal" style="max-width: 580px">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 10px">
          <h2>{{ fatura.numero }}</h2>
          <span class="badge" :class="estadoBadge(fatura.estado)">{{
            fatura.estado
          }}</span>
        </div>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="fatura-section">
          <div class="section-label">Cliente</div>
          <div class="cliente-block">
            <div class="cli-nome">{{ fatura.nomeCliente || '—' }}</div>
            <div class="cli-detail" v-if="fatura.emailCliente">
              {{ fatura.emailCliente }}
            </div>
            <div class="cli-detail" v-if="fatura.moradaCliente">
              {{ fatura.moradaCliente }}
            </div>
            <div class="cli-detail">OS #{{ fatura.ordemId }}</div>
          </div>
        </div>

        <div class="fatura-dates">
          <div>
            <div class="section-label">Data de Emissão</div>
            <div class="date-val">{{ fatura.emissao }}</div>
          </div>
          <div>
            <div class="section-label">Data de Vencimento</div>
            <div
              class="date-val"
              :class="{ vencida: isVencida(fatura) }"
            >
              {{ fatura.vencimento }}
            </div>
          </div>
        </div>

        <div class="fatura-section" v-if="fatura.ordemId">
          <div class="section-label">Ordem de Serviço</div>
          <div>{{ ordemTitulo(fatura.ordemId) }}</div>
        </div>

        <div class="fatura-section">
          <div class="section-label">Itens</div>
          <table class="itens-table">
            <thead>
              <tr>
                <th>Descrição</th>
                <th>Qtd</th>
                <th>Preço Unit.</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, i) in fatura.itens" :key="i">
                <td>{{ item.descricao }}</td>
                <td>{{ item.qty }}</td>
                <td>€{{ item.preco.toFixed(2) }}</td>
                <td>€{{ item.total.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="fatura-totals">
          <div class="total-row">
            <span>Subtotal</span
            ><span>€{{ fatura.subtotal.toFixed(2) }}</span>
          </div>
          <div class="total-row grand">
            <span>Total</span
            ><span>€{{ fatura.total.toFixed(2) }}</span>
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { Download } from "@lucide/vue"
import { useStore } from "@/store";
import { useFaturacao } from "@/composables/useFaturacao";
import { faturaBadge as estadoBadge } from "@/helpers";

const { ordensServico } = useStore();

const { downloadFaturaPDF } = useFaturacao();

const props = defineProps({
  fatura: Object,
})
defineEmits(['close'])

function download() {
  downloadFaturaPDF(props.fatura.id, props.fatura.numero)
}

function isVencida(f) {
  if (f.estado === "Paga") return false;
  const [d, m, y] = f.vencimento.split("/").map(Number);
  return new Date(y, m - 1, d) < new Date();
}

function ordemTitulo(id) {
  return ordensServico.value.find((o) => o.id === id)?.titulo || "—";
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
.fatura-dates {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}
.date-val {
  font-weight: 600;
}
.itens-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}
.itens-table th {
  text-align: left;
  padding: 7px 10px;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
}
.itens-table td {
  padding: 10px 10px;
  border-bottom: 1px solid var(--border);
}
.itens-table tr:last-child td {
  border-bottom: none;
}
.fatura-totals {
  border-top: 1px solid var(--border);
  padding-top: 12px;
  margin-top: 12px;
}
.total-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  padding: 4px 0;
  color: var(--text-muted);
}
.total-row.grand {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary);
  padding-top: 8px;
  margin-top: 4px;
  border-top: 1px solid var(--border);
}
</style>
