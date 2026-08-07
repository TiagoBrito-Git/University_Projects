<template>
  <div class="card ordem-card">
    <div class="ordem-left" @click="$emit('click', ordem)">
      <div
        class="ordem-status-dot"
        :style="{ background: estadoColor(ordem.estado) }"
      >
        <component :is="estadoIcone(ordem.estado)" :size="18" />
      </div>
      <div class="ordem-info">
        <div class="ordem-top">
          <span class="ordem-titulo">{{ ordem.descricao }}</span>
          <span class="badge" :class="estadoBadge(ordem.estado)">{{ ordem.estado }}</span>
        </div>
        <div class="ordem-meta-row">
          <span><strong>Cliente</strong> {{ ordem.clienteNome }}</span>
          <span><strong>Equipamento</strong> {{ ordem.equipamentoNome }}</span>
          <span><strong>Técnico</strong> {{ ordem.tecnico }}</span>
          <span><strong>Abertura</strong> {{ ordem.abertura }}</span>
        </div>
        <div class="ordem-valor" v-if="ordem.valorEstimado">
          Valor estimado:
          <strong style="color: var(--primary)">€{{ ordem.valorEstimado.toFixed(2) }}</strong>
        </div>
      </div>
    </div>

    <div class="ordem-actions">
      <button
        v-if="ordem.estado === 'Aguarda Diagnóstico'"
        class="btn btn-purple btn-sm"
        @click.stop="$emit('abrir-diagnostico', ordem)"
      >
        <Search :size="18" /> Registar Diagnóstico
      </button>
      <button
        v-if="ordem.estado === 'Aguarda Resposta'"
        class="btn btn-purple btn-sm"
        @click.stop="$emit('abrir-resposta', ordem)"
      >
        <MessageSquare :size="18" /> Registar Resposta
      </button>
      <button
        v-if="ordem.estado === 'Em Reparação'"
        class="btn btn-purple btn-sm"
        @click.stop="$emit('abrir-intervencao', ordem)"
      >
        <Wrench :size="18" /> Registar Intervenção
      </button>
      <button
        v-if="LABEL_AVANCAR[ordem.estado]"
        class="btn btn-success btn-sm"
        @click.stop="onAvancar"
      >
        <ArrowRight :size="18" /> {{ LABEL_AVANCAR[ordem.estado] }}
      </button>
      <button
        v-if="ordem.estado !== 'Aguarda Diagnóstico'"
        class="btn btn-secondary btn-sm"
        @click.stop="$emit('abrir-ver-diagnostico', ordem)"
      >
        <ClipboardList :size="18" /> Ver Diagnóstico
      </button>
      <button
        v-if="['Em Reparação','Aguarda Faturação','Concluído','Faturada','Encerrada'].includes(ordem.estado)"
        class="btn btn-secondary btn-sm"
        @click.stop="$emit('abrir-ver-intervencoes', ordem)"
      >
        <Settings :size="18" /> Ver Intervenções
      </button>
      <button
        v-if="ordem.estado === 'Aguarda Faturação'"
        class="btn btn-success btn-sm"
        @click.stop="$emit('pagar-fatura', ordem)"
      >
        <CreditCard :size="18" /> Pagar Fatura
      </button>
    </div>
  </div>
</template>

<script setup>

import { ArrowRight, ClipboardList, CreditCard, MessageSquare, Search, Settings, Wrench, Hourglass, DollarSign, CheckCircle, Lock, XCircle } from "@lucide/vue"
import { estadoBadge, estadoColor } from "@/helpers"
import { LABEL_AVANCAR } from "@/config/ordens-servico/constants"
import { useOS } from "@/composables/useOS";
import { useToast } from "@/composables/useToast";

const { finalizarOS, avancarProximoEstado } = useOS();
const { toast } = useToast();

const props = defineProps({
  ordem: { type: Object, required: true },
});

defineEmits(["click", "abrir-diagnostico", "abrir-resposta", "abrir-intervencao", "abrir-ver-diagnostico", "abrir-ver-intervencoes", "pagar-fatura"]);

async function onAvancar() {
  try {
    if (props.ordem.estado === "Em Reparação") {
      await finalizarOS(props.ordem.id, "Aguarda Faturação");
    } else {
      await avancarProximoEstado(props.ordem.id);
    }
    toast("OS avançada com sucesso!", "success");
  } catch (e) {
    toast(e.message);
  }
}

function estadoIcone(e) {
  const m = {
    "Aguarda Diagnóstico": Hourglass,
    "Aguarda Resposta": MessageSquare,
    "Em Reparação": Wrench,
    "Aguarda Faturação": DollarSign,
    Concluído: CheckCircle,
    Faturada: CreditCard,
    Encerrada: Lock,
    Cancelada: XCircle,
  };
  return m[e];
}
</script>

<style scoped>
.ordem-card {
  padding: 16px;
  cursor: pointer;
  transition: box-shadow var(--transition);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.ordem-card:hover {
  box-shadow: var(--shadow-md);
}
.ordem-left {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  flex: 1;
  min-width: 0;
}
.ordem-actions {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 6px;
  flex-shrink: 0;
}
.btn-success {
  background: #16a34a;
  color: white;
  border: none;
}
.btn-success:hover {
  background: #15803d;
}
.btn-sm {
  padding: 6px 12px;
  font-size: 0.78rem;
}
.ordem-status-dot {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}
.ordem-info {
  flex: 1;
  min-width: 0;
}
.ordem-top {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 4px;
}
.ordem-titulo {
  font-weight: 700;
  font-size: 0.95rem;
}
.ordem-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.ordem-meta-row strong {
  color: var(--text);
}
.ordem-valor {
  font-size: 0.8rem;
  margin-top: 6px;
  color: var(--text-muted);
}
</style>
