<template>
  <AppLayout>
    <DashboardHeader />

    <DashboardStats
      :ordensEmAberto="ordensEmAberto"
      :clientesCount="clientes.length"
      :pecasBaixoStock="pecasBaixoStock"
    />

    <div class="bottom-row">
      <DashboardOrdensRecentes :ordens="recentOrdens" />
      <DashboardAlertasStock :pecas="pecasAlerta" />
    </div>
  </AppLayout>
</template>

<script setup>
import { computed, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import DashboardHeader from "@/components/Dashboard/DashboardHeader.vue";
import DashboardStats from "@/components/Dashboard/DashboardStats.vue";
import DashboardOrdensRecentes from "@/components/Dashboard/DashboardOrdensRecentes.vue";
import DashboardAlertasStock from "@/components/Dashboard/DashboardAlertasStock.vue";
import { useStore } from "@/store";
import { useClientes } from "@/composables/useClientes";
import { useOS } from "@/composables/useOS";
import { useStock } from "@/composables/useStock";
import { ESTADOS_FINAIS } from "@/config/ordens-servico/constants";
import { MAX_RECENT_ORDENS } from "@/config/shared/constants";

const { clientes, ordensServico, pecas } = useStore();

const { fetchClientes } = useClientes();
const { fetchOrdens } = useOS();
const { fetchPecas } = useStock();

onMounted(() => {
  fetchClientes();
  fetchOrdens();
  fetchPecas();
});

const ordensEmAberto = computed(() =>
  ordensServico.value.filter((o) => !ESTADOS_FINAIS.includes(o.estado)).length
);
const pecasBaixoStock = computed(() =>
  pecas.value.filter((p) => p.stockDisponivel <= p.stockMinimo).length
);
const recentOrdens = computed(() => ordensServico.value.slice(0, MAX_RECENT_ORDENS));
const pecasAlerta = computed(() =>
  pecas.value.filter((p) => p.stockDisponivel <= p.stockMinimo)
);
</script>

<style scoped>
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 16px;
}
@media (max-width: 900px) {
  .bottom-row {
    grid-template-columns: 1fr;
  }
}
</style>
