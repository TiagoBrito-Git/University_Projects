<template>
  <AppLayout>
    <UtilizadoresHeader
      :podeGerir="podeGerirUtilizadores"
      @create="openModal()"
    />

    <UtilizadoresAcessoAlert v-if="!podeGerirUtilizadores" />

    <UtilizadoresStats :utilizadores="utilizadores" />

    <UtilizadoresFilters
      :query="query"
      :perfilFilter="perfilFilter"
      @update:query="query = $event"
      @update:perfilFilter="perfilFilter = $event"
    />

    <UtilizadoresTable
      :filtered="filtered"
      :loading="loading"
      :error="error"
      :podeGerir="podeGerirUtilizadores"
      :currentUser="currentUser"
      :desativando="desativando"
      @open="openModal"
      @desativar="confirmarDesativar"
    />

    <UtilizadorModal
      :modalOpen="modalOpen"
      :editing="editing"
      :currentUser="currentUser"
      :desativando="desativando"
      @close="closeModal"
      @desativar="confirmarDesativar"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import UtilizadoresHeader from "@/components/Utilizadores/UtilizadoresHeader.vue";
import UtilizadoresAcessoAlert from "@/components/Utilizadores/UtilizadoresAcessoAlert.vue";
import UtilizadoresStats from "@/components/Utilizadores/UtilizadoresStats.vue";
import UtilizadoresFilters from "@/components/Utilizadores/UtilizadoresFilters.vue";
import UtilizadoresTable from "@/components/Utilizadores/UtilizadoresTable.vue";
import UtilizadorModal from "@/components/Utilizadores/UtilizadorModal.vue";
import { useAuth } from "@/composables/useAuth";
import { useUtilizadores } from "@/composables/useUtilizadores";
import { PERFIS_GERIVEIS } from "@/config/utilizadores/constants";
import { useToast } from "@/composables/useToast";

const { currentUser } = useAuth();
const { toast } = useToast();

const { utilizadores, loading, error, fetchUtilizadores, createUtilizador, updateUtilizador, desativarUtilizador } =
  useUtilizadores();

const query = ref("");
const perfilFilter = ref("");
const modalOpen = ref(false);
const editing = ref(null);
const desativando = ref(false);

onMounted(() => {
  fetchUtilizadores();
});

const podeGerirUtilizadores = computed(() => {
  const perfil = currentUser.value?.perfil;
  return PERFIS_GERIVEIS.includes(perfil);
});

const filtered = computed(() => {
  let list = utilizadores.value;
  if (perfilFilter.value) {
    list = list.filter((u) => u.perfil === perfilFilter.value);
  }
  if (query.value) {
    const q = query.value.toLowerCase();
    list = list.filter(
      (u) =>
        u.nome.toLowerCase().includes(q) || u.username.toLowerCase().includes(q)
    );
  }
  return list;
});

function closeModal() {
  modalOpen.value = false;
  fetchUtilizadores();
}

function openModal(u = null) {
  editing.value = u;
  modalOpen.value = true;
}

async function confirmarDesativar(u, event) {
  event?.stopPropagation();
  if (!confirm(`Desativar a conta de "${u.nome}"?\nO utilizador deixará de conseguir entrar no sistema, mas o histórico é preservado.`)) return;
  desativando.value = true;
  try {
    await desativarUtilizador(u.id);
    if (modalOpen.value && editing.value?.id === u.id) modalOpen.value = false;
  } catch (err) {
    toast(err.message);
  } finally {
    desativando.value = false;
  }
}
</script>
