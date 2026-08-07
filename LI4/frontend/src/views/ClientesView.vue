<template>
  <AppLayout>
    <ClienteHeader @create="openModal()" />

    <ClienteSearch v-model:query="query" />

    <div class="clientes-grid">
      <ClienteCard
        v-for="cliente in filtered"
        :key="cliente.id"
        :cliente="cliente"
        @click="openModal(cliente)"
      />
    </div>

    <div v-if="filtered.length === 0" class="empty-state">
      Nenhum cliente encontrado.
    </div>

    <ClienteModal
      :modalOpen="modalOpen"
      :editing="editing"
      :form="form"
      @close="modalOpen = false"
      @save="saveCliente"
      @delete="handleDelete"
      @update:form="onFormUpdate"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import ClienteHeader from "@/components/Clientes/ClienteHeader.vue";
import ClienteSearch from "@/components/Clientes/ClienteSearch.vue";
import ClienteCard from "@/components/Clientes/ClienteCard.vue";
import ClienteModal from "@/components/Clientes/ClienteModal.vue";
import { useStore } from "@/store";
import { useClientes } from "@/composables/useClientes";
import { useToast } from "@/composables/useToast";

const { toast } = useToast();

const { clientes } = useStore();

const query = ref("");
const modalOpen = ref(false);
const editing = ref(null);

const {
  loading,
  error,
  fetchClientes,
  updateCliente,
  createCliente,
  deleteCliente,
} = useClientes();

onMounted(() => {
  fetchClientes();
});

const form = reactive({
  nome: "",
  email: "",
  telefone: "",
  morada: "",
  nif: "",
});

const filtered = computed(() => {
  if (!query.value) return clientes.value;
  const q = query.value.toLowerCase();
  return clientes.value.filter(
    (c) =>
      c.nome.toLowerCase().includes(q) ||
      c.email.toLowerCase().includes(q) ||
      c.telefone.includes(q) ||
      (c.nif && c.nif.toString().includes(q))
  );
});

function onFormUpdate(newForm) {
  Object.assign(form, newForm);
}

function openModal(cliente = null) {
  editing.value = cliente;
  if (cliente) {
    Object.assign(form, {
      nome: cliente.nome,
      email: cliente.email,
      telefone: cliente.telefone,
      morada: cliente.morada,
      nif: cliente.nif,
    });
  } else {
    Object.assign(form, {
      nome: "",
      email: "",
      telefone: "",
      morada: "",
      nif: "",
    });
  }
  modalOpen.value = true;
}

async function saveCliente() {
  if (!form.nome) { toast("O nome é obrigatório.", "warning"); return }
  if (!form.nif) { toast("O NIF é obrigatório.", "warning"); return }
  if (!/^\d{9}$/.test(form.nif)) { toast("O NIF deve ter exatamente 9 dígitos.", "warning"); return }
  if (!form.telefone) { toast("O contacto é obrigatório.", "warning"); return }
  if (!/^\d{9}$/.test(form.telefone)) { toast("O contacto deve ter exatamente 9 dígitos.", "warning"); return }

  const payload = {
    nome: form.nome,
    nif: form.nif,
    contacto: form.telefone,
    email: form.email,
    morada: form.morada,
  };

  try {
    if (editing.value) {
      await updateCliente(editing.value.id, payload);
    } else {
      await createCliente(payload);
    }
    modalOpen.value = false;
    toast("Cliente guardado com sucesso!", "success");
  } catch (err) {
    toast(err.message);
  }
}

async function handleDelete() {
  if (editing.value) {
    await deleteCliente(editing.value.id);
    modalOpen.value = false;
  }
}
</script>

<style scoped>
.clientes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.empty-state {
  text-align: center;
  color: var(--text-muted);
  padding: 48px;
  font-size: 0.9rem;
}
</style>
