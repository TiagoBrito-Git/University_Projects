<template>
  <AppLayout>
    <FaturacaoHeader @create="openCreate" />

    <FaturacaoStats
      :totalFaturas="faturas.length"
      :receitaRecebida="receitaRecebida"
      :porPagar="porPagar"
      :vencidas="vencidas"
    />

    <FaturacaoFilters
      v-model:query="query"
      v-model:tabFilter="tabFilter"
      :estadoTabs="estadoTabs"
    />

    <FaturasTable
      :filtered="filtered"
      @view="viewFatura"
    />

    <FaturaDetailModal
      :fatura="selectedFatura"
      @close="selectedFatura = null"
    />

    <FaturaCreateModal
      :modalOpen="createModal"
      :storeClientes="clientes"
      :storeOrdensServico="ordensServico"
      @close="closeCreateModal"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import FaturacaoHeader from "@/components/Faturacao/FaturacaoHeader.vue";
import FaturacaoStats from "@/components/Faturacao/FaturacaoStats.vue";
import FaturacaoFilters from "@/components/Faturacao/FaturacaoFilters.vue";
import FaturasTable from "@/components/Faturacao/FaturasTable.vue";
import FaturaDetailModal from "@/components/Faturacao/FaturaDetailModal.vue";
import FaturaCreateModal from "@/components/Faturacao/FaturaCreateModal.vue";
import { useStore } from "@/store";
import { useFaturacao } from "@/composables/useFaturacao";
import { ESTADOS_FATURA } from "@/config/faturacao/constants";

const { faturas, clientes, ordensServico } = useStore();

const {
  loading,
  error,
  fetchFaturas,
} = useFaturacao();

const query = ref("");
const tabFilter = ref("Todas");
const selectedFatura = ref(null);
const createModal = ref(false);

const estadoTabs = ["Todas", ...ESTADOS_FATURA];

const receitaRecebida = computed(() =>
  faturas.value
    .filter((f) => f.estado === "Paga")
    .reduce((s, f) => s + f.total, 0)
);
const porPagar = computed(
  () => faturas.value.filter((f) => f.estado === "Emitida").length
);
const vencidas = computed(
  () => faturas.value.filter((f) => isVencida(f) && f.estado !== "Paga").length
);

const filtered = computed(() => {
  let list = faturas.value;
  if (tabFilter.value !== "Todas")
    list = list.filter((f) => f.estado === tabFilter.value);
  if (query.value)
    list = list.filter((f) =>
      f.numero.toLowerCase().includes(query.value.toLowerCase())
    );
  return list;
});

onMounted(() => {
  fetchFaturas();
});

function viewFatura(f) {
  selectedFatura.value = f;
}

function openCreate() {
  createModal.value = true;
}

function closeCreateModal() {
  createModal.value = false;
  fetchFaturas();
}

function isVencida(f) {
  if (f.estado === "Paga") return false;
  const [d, m, y] = f.vencimento.split("/").map(Number);
  return new Date(y, m - 1, d) < new Date();
}

</script>

<style scoped>
.btn-success {
  background: var(--success);
  color: #fff;
  border: none;
}
.btn-success:hover {
  opacity: 0.88;
}
</style>
