<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ editingOrdem ? "Editar Ordem" : "Nova Ordem de Serviço" }}</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-row">
          <div class="form-group">
            <label>Número de Série da Trotinete</label>
            <div class="autocomplete-wrap">
              <input
                v-model="serieSearch"
                class="form-control"
                placeholder="Ex: XM-2024-001"
                @input="showSerieSuggestions = true"
                @blur="hideSerieSuggestions"
                autocomplete="off"
              />
              <ul
                v-if="showSerieSuggestions && serieSuggestions.length"
                class="autocomplete-list"
              >
                <li
                  v-for="t in serieSuggestions"
                  :key="t.id"
                  @mousedown.prevent="selectTrotinete(t)"
                >
                  <span class="sug-serie">{{ t.serie }}</span>
                  <span class="sug-modelo">{{ t.marca }} {{ t.modelo }}</span>
                </li>
              </ul>
            </div>
          </div>
          <div class="form-group">
            <label>NIF do Cliente</label>
            <input
              v-model="form.clienteNif"
              class="form-control nif-readonly"
              placeholder="Preenchido automaticamente"
              readonly
            />
          </div>
        </div>
        <div class="form-group">
          <label>Descrição do Problema <span class="required">*</span></label>
          <textarea v-model="form.descricao" class="form-control" rows="3"></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Técnico <span class="required">*</span></label>
            <select v-model="form.idTecnico" class="form-control">
              <option value="" disabled>Selecionar técnico...</option>
              <option
                v-for="u in tecnicos"
                :key="u.id"
                :value="u.id"
              >
                {{ u.nome }}
              </option>
            </select>
          </div>
        </div>
        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px">
          <button class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button class="btn btn-primary" @click="saveOrdem">
            {{ editingOrdem ? "Guardar" : "Criar" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { useOS } from "@/composables/useOS";
import { MAX_SUGGESTIONS } from "@/config/shared/constants";
import { useToast } from "@/composables/useToast";
const { createOrdem, updateOrdem } = useOS();
const { toast } = useToast();

const props = defineProps({
  modalOpen: { type: Boolean, default: false },
  editingOrdem: { type: Object, default: null },
  tecnicos: { type: Array, default: () => [] },
  trotinetes: { type: Array, default: () => [] },
  storeClientes: { type: Array, default: () => [] },
});

const emit = defineEmits(["close"]);

const form = reactive({
  clienteNif: "",
  numeroSerie: "",
  descricao: "",
  idTecnico: "",
});

const serieSearch = ref("");
const showSerieSuggestions = ref(false);

const serieSuggestions = computed(() => {
  if (!serieSearch.value.trim()) return [];
  const q = serieSearch.value.toLowerCase();
  return props.trotinetes
    .filter((t) => t.serie.toLowerCase().includes(q))
    .slice(0, MAX_SUGGESTIONS);
});

function selectTrotinete(t) {
  form.numeroSerie = t.serie;
  serieSearch.value = t.serie;
  showSerieSuggestions.value = false;
  const cliente = props.storeClientes.find((c) => c.id === t.clienteId);
  form.clienteNif = cliente?.nif ?? "";
}

function hideSerieSuggestions() {
  setTimeout(() => { showSerieSuggestions.value = false; }, 150);
}

async function saveOrdem() {
  if (!form.descricao.trim()) { toast("A descrição é obrigatória.", "warning"); return }
  if (!form.clienteNif) { toast("Selecione uma trotinete (cliente é preenchido automaticamente).", "warning"); return }
  if (!form.numeroSerie) { toast("O número de série da trotinete é obrigatório.", "warning"); return }
  if (!form.idTecnico) { toast("Selecione um técnico.", "warning"); return }

  const dados = {
    descricao: form.descricao,
    nif_cliente: form.clienteNif,
    n_serie_trotinete: form.numeroSerie,
    id_tecnico: Number(form.idTecnico),
  };
  try {
    if (props.editingOrdem) {
      await updateOrdem({ id: props.editingOrdem.id, descricao: dados.descricao });
    } else {
      await createOrdem(dados);
    }
    emit("close");
    toast("Ordem de serviço guardada com sucesso!", "success");
  } catch (err) {
    toast(err.message);
  }
}
</script>

<style scoped>
.required {
  color: var(--danger);
}
.autocomplete-wrap {
  position: relative;
}
.autocomplete-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 200;
  background: white;
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
  max-height: 220px;
  overflow-y: auto;
  list-style: none;
  margin: 0;
  padding: 0;
  box-shadow: var(--shadow-sm);
}
.autocomplete-list li {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background var(--transition);
}
.autocomplete-list li:hover {
  background: var(--bg);
}
.sug-serie {
  font-weight: 700;
  font-size: 0.875rem;
  font-family: "DM Mono", monospace;
  color: var(--text);
}
.sug-modelo {
  font-size: 0.75rem;
  color: var(--text-muted);
}
.nif-readonly {
  background: var(--bg);
  color: var(--text-muted);
  cursor: default;
}
</style>
