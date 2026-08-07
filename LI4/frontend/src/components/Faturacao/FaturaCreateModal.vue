<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>Nova Fatura</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Ordem de Serviço</label>
          <select v-model="form.ordemId" class="form-control">
            <option :value="null">— Nenhuma —</option>
            <option
              v-for="o in storeOrdensServico"
              :key="o.id"
              :value="o.id"
            >
              {{ o.titulo }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>Descrição do Serviço</label>
          <input
            v-model="form.descricao"
            class="form-control"
            placeholder="Ex: Manutenção preventiva"
          />
        </div>
        <div class="form-group">
          <label>Valor (€)</label>
          <input
            v-model.number="form.valor"
            type="number"
            min="0"
            step="0.01"
            class="form-control"
          />
        </div>
        <div class="alert-erro" v-if="formError">{{ formError }}</div>
        <div
          style="
            display: flex;
            gap: 8px;
            justify-content: flex-end;
            margin-top: 8px;
          "
        >
          <button class="btn btn-secondary" @click="$emit('close')">
            Cancelar
          </button>
          <button class="btn btn-primary" :disabled="saving" @click="save">
            {{ saving ? "A criar…" : "Criar Fatura" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, ref } from "vue";
import { API_BASE, authFetch } from "@/api";

const props = defineProps({
  modalOpen: Boolean,
  storeClientes: Array,
  storeOrdensServico: Array,
})
const emit = defineEmits(['close'])

const saving = ref(false)
const formError = ref("")
const form = reactive({
  ordemId: null,
  descricao: "",
  valor: 0,
})

watch(() => props.modalOpen, (open) => {
  if (open) {
    formError.value = ""
    Object.assign(form, {
      ordemId: props.storeOrdensServico?.[0]?.id ?? null,
      descricao: "",
      valor: 0,
    });
  }
})

async function save() {
  formError.value = ""
  if (!form.ordemId) {
    formError.value = "Selecione uma ordem de serviço."
    return
  }
  if (form.valor <= 0) {
    formError.value = "O valor deve ser superior a 0."
    return
  }
  saving.value = true
  try {
    const res = await authFetch(`${API_BASE}/fatura/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id_os: form.ordemId,
        descricao: form.descricao,
        valor: form.valor,
      }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Erro ao criar fatura");
    }
    emit('close')
  } catch (e) {
    formError.value = e.message
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 5px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}
.form-control {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  outline: none;
  transition: border-color var(--transition);
  background: var(--surface);
  color: var(--text);
}
.form-control:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(26, 86, 219, 0.1);
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.alert-erro {
  margin-top: 10px;
  padding: 10px 14px;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-left: 3px solid var(--danger);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: #be123c;
}
</style>
