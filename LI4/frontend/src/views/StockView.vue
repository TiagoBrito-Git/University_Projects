<template>
  <AppLayout>
    <StockHeader @create="openModal()" />

    <StockStats
      :totalItens="pecas.length"
      :alertas="alertas"
      :valorTotal="valorTotal"
      :categoriasCount="categorias.length"
    />

    <StockAlertas v-if="alertasPecas.length > 0" :alertasPecas="alertasPecas" />

    <StockFilters
      v-model:query="query"
      v-model:catFilter="catFilter"
      :categorias="categorias"
    />

    <div class="pecas-grid">
      <PecaCard
        v-for="peca in filtered"
        :key="peca.id"
        :peca="peca"
        @click="openModal(peca)"
      />
    </div>

    <div v-if="filtered.length === 0" class="empty-state">
      Nenhuma peça encontrada.
    </div>

    <StockModal
      :modalOpen="modalOpen"
      :editing="editing"
      :form="form"
      @close="modalOpen = false"
      @save="savePeca"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import StockHeader from "@/components/Stock/StockHeader.vue";
import StockStats from "@/components/Stock/StockStats.vue";
import StockAlertas from "@/components/Stock/StockAlertas.vue";
import StockFilters from "@/components/Stock/StockFilters.vue";
import PecaCard from "@/components/Stock/PecaCard.vue";
import StockModal from "@/components/Stock/StockModal.vue";
import { useStore } from "@/store";
import { useStock } from "@/composables/useStock";

const { pecas } = useStore();

const {
  fetchPecas,
  createPeca,
  updatePeca,
} = useStock();
import { useToast } from "@/composables/useToast";

const { toast } = useToast();

const query = ref("");
const catFilter = ref("Todas");
const modalOpen = ref(false);
const editing = ref(null);

const form = reactive({
  nome: "",
  codigo: "",
  descricao: "",
  categoria: "Eletrónica",
  fornecedor: "",
  precoUnitario: 0,
  stockDisponivel: 0,
  stockMinimo: 0,
});

const categorias = computed(() => [
  ...new Set(pecas.value.map((p) => p.categoria)),
]);
const alertasPecas = computed(() =>
  pecas.value.filter((p) => p.stockDisponivel <= p.stockMinimo)
);
const alertas = computed(() => alertasPecas.value.length);
const valorTotal = computed(() =>
  pecas.value.reduce((s, p) => s + p.precoUnitario * p.stockDisponivel, 0)
);

const filtered = computed(() => {
  let list = pecas.value;
  if (catFilter.value !== "Todas")
    list = list.filter((p) => p.categoria === catFilter.value);
  if (query.value) {
    const q = query.value.toLowerCase();
    list = list.filter((p) =>
      `${p.nome} ${p.codigo} ${p.descricao}`.toLowerCase().includes(q)
    );
  }
  return list;
});

onMounted(() => {
  fetchPecas();
});

function openModal(peca = null) {
  editing.value = peca;
  if (peca) {
    Object.assign(form, {
      nome: peca.nome,
      codigo: peca.codigo,
      descricao: peca.descricao,
      categoria: peca.categoria,
      fornecedor: peca.fornecedor,
      precoUnitario: peca.precoUnitario,
      stockDisponivel: peca.stockDisponivel,
      stockMinimo: peca.stockMinimo,
    });
  } else {
    Object.assign(form, {
      nome: "",
      codigo: "",
      descricao: "",
      categoria: "Eletrónica",
      fornecedor: "",
      precoUnitario: 0,
      stockDisponivel: 0,
      stockMinimo: 0,
    });
  }
  modalOpen.value = true;
}

async function savePeca() {
  if (!form.nome) { toast("O nome é obrigatório.", "warning"); return }
  if (!form.codigo) { toast("O código é obrigatório.", "warning"); return }

  const payload = {
    nome: form.nome,
    codigo: form.codigo,
    descricao: form.descricao,
    fornecedor: form.fornecedor,
    categoria: form.categoria,
    stock: parseInt(form.stockDisponivel) || 0,
    stock_minimo: parseInt(form.stockMinimo) || 0,
    preco: parseFloat(form.precoUnitario) || 0
  };

  try {
    if (editing.value) {
      await updatePeca(editing.value.codigo, payload);
    } else {
      await createPeca(payload);
    }
    modalOpen.value = false;
    await fetchPecas();
    toast("Peça guardada com sucesso!", "success");
  } catch (err) {
    toast(err.message);
  }
}
</script>

<style scoped>
.pecas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.empty-state {
  text-align: center;
  color: var(--text-muted);
  padding: 48px;
  font-size: 0.9rem;
}
</style>
