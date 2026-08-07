<template>
  <AppLayout>
    <EquipamentoHeader @create="openModal()" />

    <div class="filters-row">
      <EquipamentoSearch :query="query" @update:query="query = $event" />
    </div>

    <div class="equip-grid">
      <EquipamentoCard
        v-for="eq in filtered"
        :key="eq.id"
        :equipamento="eq"
        :clienteNome="clienteNome(eq.clienteId)"
        @click="openModal"
        @remove="confirmarRemover"
      />
    </div>

    <div v-if="filtered.length === 0" class="empty-state">
      Nenhum equipamento encontrado.
    </div>

    <EquipamentoModal
      :modalOpen="modalOpen"
      :editing="editing"
      :form="form"
      :clienteSearch="clienteSearch"
      :showSuggestions="showSuggestions"
      :clienteSuggestions="clienteSuggestions"
      @close="modalOpen = false"
      @save="save"
      @remove="confirmarRemover(editing); modalOpen = false"
      @update:marca="form.marca = $event"
      @update:modelo="form.modelo = $event"
      @update:serie="form.serie = $event"
      @update:clienteSearch="clienteSearch = $event"
      @update:showSuggestions="showSuggestions = $event"
      @select-cliente="selectCliente"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import EquipamentoHeader from "@/components/Equipamentos/EquipamentoHeader.vue";
import EquipamentoSearch from "@/components/Equipamentos/EquipamentoSearch.vue";
import EquipamentoCard from "@/components/Equipamentos/EquipamentoCard.vue";
import EquipamentoModal from "@/components/Equipamentos/EquipamentoModal.vue";
import { useStore } from "@/store";
import { useTrotinetes } from "@/composables/useTrotinetes";
import { MAX_SUGGESTIONS } from "@/config/shared/constants";

const { clientes } = useStore();
import { useClientes } from "@/composables/useClientes";

const {
  trotinetes,
  fetchTrotinetes,
  createTrotinete,
  updateTrotinete,
  deleteTrotinete,
} = useTrotinetes();
const { fetchClientes } = useClientes();
import { useToast } from "@/composables/useToast";

const { toast } = useToast();

const query = ref("");
const modalOpen = ref(false);
const editing = ref(null);

const form = reactive({
  marca: "",
  modelo: "",
  serie: "",
  clienteId: null,
});

const clienteSearch = ref("");
const showSuggestions = ref(false);

const clienteSuggestions = computed(() => {
  if (!clienteSearch.value.trim()) return clientes.value.slice(0, MAX_SUGGESTIONS);
  const q = clienteSearch.value.toLowerCase();
  return clientes.value.filter((c) => c.nome.toLowerCase().includes(q)).slice(0, MAX_SUGGESTIONS);
});

function selectCliente(c) {
  form.clienteId = c.id;
  clienteSearch.value = c.nome;
  showSuggestions.value = false;
}

onMounted(() => {
  fetchTrotinetes();
  fetchClientes();
});

const filtered = computed(() => {
  let list = trotinetes.value;
  if (query.value) {
    const q = query.value.toLowerCase();
    list = list.filter((e) =>
      `${e.marca} ${e.modelo} ${e.serie}`.toLowerCase().includes(q)
    );
  }
  return list;
});

function clienteNome(id) {
  return clientes.value.find((c) => c.id === id)?.nome || "—";
}

function openModal(eq = null) {
  editing.value = eq;
  if (eq) {
    Object.assign(form, {
      marca: eq.marca,
      modelo: eq.modelo,
      serie: eq.serie,
      clienteId: eq.clienteId,
    });
    clienteSearch.value = clienteNome(eq.clienteId);
  } else {
    Object.assign(form, {
      marca: "",
      modelo: "",
      serie: "",
      clienteId: null,
    });
    clienteSearch.value = "";
  }
  showSuggestions.value = false;
  modalOpen.value = true;
}

async function save() {
  if (!form.marca || !form.modelo || !form.serie || !form.clienteId) {
    toast("Por favor, preencha todos os campos obrigatórios.", "warning");
    return;
  }
  const payload = {
    marca: form.marca,
    modelo: form.modelo,
    serie: form.serie,
    clienteId: form.clienteId,
  };
  try {
    if (editing.value) {
      await updateTrotinete(editing.value.id, payload);
    } else {
      await createTrotinete(payload);
    }
    modalOpen.value = false;
    toast("Equipamento guardado com sucesso!", "success");
  } catch (err) {
    toast(err.message);
  }
}

async function confirmarRemover(eq) {
  if (!confirm(`Remover "${eq.marca} ${eq.modelo}" (${eq.serie})?`)) return;
  try {
    await deleteTrotinete(eq.id);
  } catch (err) {
    toast(err.message);
  }
}
</script>

<style scoped>
.filters-row {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.equip-grid {
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
