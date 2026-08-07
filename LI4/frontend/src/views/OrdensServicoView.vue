<template>
  <AppLayout>
    <OSHeader @create="openCreate" />

    <OSStats
      :emAberto="kpis.emAberto"
      :concluidas="kpis.concluidas"
      :emReparacao="kpis.emReparacao"
      :aguardaFaturacao="kpis.aguardaFaturacao"
    />

    <OSFilters
      :query="query"
      :estadoFilter="estadoFilter"
      :activeTab="activeTab"
      :tabs="tabs"
      @update:query="query = $event"
      @update:estadoFilter="estadoFilter = $event"
      @update:activeTab="activeTab = $event"
    />

    <div class="ordem-list">
      <OSCard
        v-for="ordem in filteredOrdens"
        :key="ordem.id"
        :ordem="ordem"
        @click="abrirDetalhes"
        @abrir-diagnostico="abrirDiagnostico"
        @abrir-resposta="abrirResposta"
        @abrir-intervencao="abrirIntervencao"
        @abrir-ver-diagnostico="abrirVerDiagnostico"
        @abrir-ver-intervencoes="abrirVerIntervencoes"
        @pagar-fatura="handlePagarFatura"
      />
      <div v-if="filteredOrdens.length === 0" class="empty-state">
        Nenhuma ordem encontrada.
      </div>
    </div>

    <OSDetailModal
      :ordem="selectedOrdem"
      @close="selectedOrdem = null"
      @abrir-diagnostico="abrirDiagnostico"
      @abrir-resposta="abrirResposta"
      @abrir-intervencao="abrirIntervencao"
      @abrir-ver-diagnostico="abrirVerDiagnostico"
      @abrir-ver-intervencoes="abrirVerIntervencoes"
    />

    <OSDiagnosticoModal
      :modalOpen="diagnosticoModal"
      :ordem="ordemEmDiagnostico"
      :pecasDisponiveis="pecas"
      :taxaMaoObra="taxaMaoObra"
      @close="fecharModal"
    />

    <OSRespostaModal
      :modalOpen="respostaModal"
      :ordem="ordemEmResposta"
      @close="fecharRespostaModal"
    />

    <OSIntervencaoModal
      :modalOpen="intervencaoModal"
      :ordem="ordemEmIntervencao"
      :pecasDisponiveis="pecas"
      :taxaMaoObra="taxaMaoObra"
      @close="fecharIntervencaoModal"
    />

    <OSVerDiagnosticoModal
      :ordem="osParaVer"
      @close="verDiagnosticoModal = false"
      v-if="verDiagnosticoModal"
    />

    <OSVerIntervencoesModal
      :ordem="osParaVer"
      @close="verIntervencoesModal = false"
      v-if="verIntervencoesModal"
    />

    <OSCreateModal
      :modalOpen="createModal"
      :editingOrdem="editingOrdem"
      :tecnicos="tecnicos"
      :trotinetes="trotinetes"
      :storeClientes="clientes"
      @close="createModal = false"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import OSHeader from "@/components/OrdensServico/OSHeader.vue";
import OSStats from "@/components/OrdensServico/OSStats.vue";
import OSFilters from "@/components/OrdensServico/OSFilters.vue";
import OSCard from "@/components/OrdensServico/OSCard.vue";
import OSDetailModal from "@/components/OrdensServico/OSDetailModal.vue";
import OSDiagnosticoModal from "@/components/OrdensServico/OSDiagnosticoModal.vue";
import OSRespostaModal from "@/components/OrdensServico/OSRespostaModal.vue";
import OSIntervencaoModal from "@/components/OrdensServico/OSIntervencaoModal.vue";
import OSVerDiagnosticoModal from "@/components/OrdensServico/OSVerDiagnosticoModal.vue";
import OSVerIntervencoesModal from "@/components/OrdensServico/OSVerIntervencoesModal.vue";
import OSCreateModal from "@/components/OrdensServico/OSCreateModal.vue";
import { useStore } from "@/store";
import { useOS } from "@/composables/useOS";

const { ordensServico, faturas, pecas, clientes } = useStore();
import { useUtilizadores } from "@/composables/useUtilizadores";
import { useFaturacao } from "@/composables/useFaturacao";
import { useTrotinetes } from "@/composables/useTrotinetes";
import { useToast } from "@/composables/useToast";

const { toast } = useToast();
import { useClientes } from "@/composables/useClientes";
import { ESTADOS_FINAIS, TAB_ESTADOS } from "@/config/ordens-servico/constants";
import { DEFAULT_TAXA_MAO_OBRA } from "@/config/shared/constants";

const query = ref("");
const estadoFilter = ref("");
const activeTab = ref("all");
const selectedOrdem = ref(null);
const createModal = ref(false);
const editingOrdem = ref(null);

const { ordemSelecionada, ordens, loading, error, fetchOrdens, fetchDetalhesOS, fetchConfig, pagarFatura } = useOS();

const { fetchFaturas } = useFaturacao();
const { utilizadores, fetchUtilizadores } = useUtilizadores();
const { trotinetes, fetchTrotinetes } = useTrotinetes();
const { fetchClientes } = useClientes();

const tecnicos = computed(() => utilizadores.value.filter(u => u.perfil === "tecnico"));
const taxaMaoObra = ref(DEFAULT_TAXA_MAO_OBRA);

onMounted(async () => {
  fetchOrdens();
  fetchUtilizadores();
  fetchTrotinetes();
  fetchClientes();
  const config = await fetchConfig();
  taxaMaoObra.value = config.taxa_mao_obra;
});

const kpis = computed(() => ({
  emAberto: ordensServico.value.filter((o) => !ESTADOS_FINAIS.includes(o.estado)).length,
  concluidas: ordensServico.value.filter((o) => ["Concluído", "Faturada", "Encerrada"].includes(o.estado)).length,
  emReparacao: ordensServico.value.filter((o) => o.estado === "Em Reparação").length,
  aguardaFaturacao: ordensServico.value.filter((o) => o.estado === "Aguarda Faturação").length,
}));

const tabs = computed(() => {
  const counts = {};
  ordensServico.value.forEach(o => {
    counts[o.estado] = (counts[o.estado] || 0) + 1;
  });
  return [
    { key: "all", label: "Todas", count: ordensServico.value.length },
    ...Object.entries(TAB_ESTADOS).map(([key, estado]) => ({
      key, label: estado, count: counts[estado] || 0,
    })),
  ];
});

const allOrdens = computed(() => {
  let list = ordensServico.value;
  if (estadoFilter.value) list = list.filter((o) => o.estado === estadoFilter.value);
  if (query.value) {
    const q = query.value.toLowerCase();
    list = list.filter((o) =>
      o.descricao?.toLowerCase().includes(q) ||
      o.id.toString().includes(q) ||
      o.estado.toLowerCase().includes(q) ||
      o.clienteNome?.toLowerCase().includes(q)
    );
  }
  return list;
});

const filteredOrdens = computed(() => {
  if (activeTab.value === "all") return allOrdens.value;
  return allOrdens.value.filter((o) => o.estado === TAB_ESTADOS[activeTab.value]);
});

const handlePagarFatura = async (ordem) => {
  try {
    await fetchFaturas();
    const fatura = faturas.value.find(f => f.ordemId === ordem.id && f.estado === "Emitida");
    if (!fatura) {
      toast("Nenhuma fatura pendente encontrada para esta OS.", "warning");
      return;
    }
    await pagarFatura(fatura.id);
    toast("Fatura paga e OS encerrada com sucesso!", "success");
  } catch (e) {
    toast(e.message);
  }
};

async function abrirDetalhes(ordem) {
  selectedOrdem.value = ordem;
  await fetchDetalhesOS(ordem.id);
  selectedOrdem.value = ordemSelecionada.value;
}

// Modal de diagnóstico
const diagnosticoModal = ref(false);
const ordemEmDiagnostico = ref(null);

function abrirDiagnostico(ordem) {
  ordemEmDiagnostico.value = ordem;
  selectedOrdem.value = null;
  diagnosticoModal.value = true;
}

function fecharModal() {
  diagnosticoModal.value = false;
  ordemEmDiagnostico.value = null;
}

// Modal de resposta
const respostaModal = ref(false);
const ordemEmResposta = ref(null);

function abrirResposta(ordem) {
  ordemEmResposta.value = ordem;
  selectedOrdem.value = null;
  respostaModal.value = true;
}

function fecharRespostaModal() {
  respostaModal.value = false;
  ordemEmResposta.value = null;
}

// Modal de intervenção
const intervencaoModal = ref(false);
const ordemEmIntervencao = ref(null);

function abrirIntervencao(ordem) {
  ordemEmIntervencao.value = ordem;
  selectedOrdem.value = null;
  intervencaoModal.value = true;
}

function fecharIntervencaoModal() {
  intervencaoModal.value = false;
  ordemEmIntervencao.value = null;
}

// Modais de leitura
const verDiagnosticoModal = ref(false);
const verIntervencoesModal = ref(false);
const osParaVer = ref(null);

async function abrirVerDiagnostico(ordem) {
  selectedOrdem.value = null;
  await fetchDetalhesOS(ordem.id);
  osParaVer.value = ordemSelecionada.value;
  verDiagnosticoModal.value = true;
}

async function abrirVerIntervencoes(ordem) {
  selectedOrdem.value = null;
  await fetchDetalhesOS(ordem.id);
  osParaVer.value = ordemSelecionada.value;
  verIntervencoesModal.value = true;
}

function openCreate() {
  editingOrdem.value = null;
  createModal.value = true;
}


</script>

<style scoped>
.ordem-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.empty-state {
  text-align: center;
  color: var(--text-muted);
  padding: 48px;
  font-size: 0.9rem;
}
</style>
