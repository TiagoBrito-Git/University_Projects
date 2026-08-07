<template>
  <AppLayout>
    <RelatoriosHeader />

    <RelatoriosStats
      :relatorios="relatorios"
    />

    <RelatoriosFilters
      v-model:query="query"
      v-model:tabFilter="tabFilter"
      :tipoTabs="tipoTabs"
    />

    <RelatoriosTable
      :relatorios="relatorios"
      :filtered="filtered"
      :loading="loading"
      :error="error"
      @view="viewRelatorio"
    />

    <RelatorioDetailModal
      :relatorio="selectedRelatorio"
      @close="selectedRelatorio = null"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import RelatoriosHeader from "@/components/Relatorios/RelatoriosHeader.vue";
import RelatoriosStats from "@/components/Relatorios/RelatoriosStats.vue";
import RelatoriosFilters from "@/components/Relatorios/RelatoriosFilters.vue";
import RelatoriosTable from "@/components/Relatorios/RelatoriosTable.vue";
import RelatorioDetailModal from "@/components/Relatorios/RelatorioDetailModal.vue";
import { useRelatorios } from "@/composables/useRelatorios";

const { relatorios, loading, error, fetchRelatorios } = useRelatorios();

const query = ref("");
const tabFilter = ref("Todos");
const selectedRelatorio = ref(null);

const tipoTabs = ["Todos", "Económico", "Stock", "Performance"];

const filtered = computed(() => {
  let list = relatorios.value;
  if (tabFilter.value !== "Todos")
    list = list.filter((r) => r.tipo_relatorio === tabFilter.value);
  if (query.value)
    list = list.filter((r) =>
      r.nome_arquivo.toLowerCase().includes(query.value.toLowerCase())
    );
  return list;
});

function viewRelatorio(r) {
  selectedRelatorio.value = r;
}

onMounted(() => {
  fetchRelatorios();
});
</script>

