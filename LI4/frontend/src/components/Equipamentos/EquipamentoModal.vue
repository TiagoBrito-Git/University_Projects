<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ editing ? "Editar Equipamento" : "Novo Equipamento" }}</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-row">
          <div class="form-group">
            <label>Marca</label>
            <input
              :value="form.marca"
              @input="$emit('update:marca', $event.target.value)"
              class="form-control"
              placeholder="Ex: Xiaomi"
            />
          </div>
          <div class="form-group">
            <label>Modelo</label>
            <input
              :value="form.modelo"
              @input="$emit('update:modelo', $event.target.value)"
              class="form-control"
              placeholder="Ex: Mi Scooter Pro 2"
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Nº Série</label>
            <input
              :value="form.serie"
              @input="$emit('update:serie', $event.target.value)"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label>Cliente</label>
            <div class="autocomplete-wrap">
              <input
                :value="clienteSearch"
                @input="$emit('update:clienteSearch', $event.target.value); $emit('update:showSuggestions', true)"
                @blur="setTimeout(() => $emit('update:showSuggestions', false), 150)"
                class="form-control"
                placeholder="Pesquisar cliente..."
                autocomplete="off"
              />
              <ul
                v-if="showSuggestions && clienteSuggestions.length"
                class="autocomplete-list"
              >
                <li
                  v-for="c in clienteSuggestions"
                  :key="c.id"
                  @mousedown.prevent="$emit('select-cliente', c)"
                >
                  {{ c.nome }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px;">
          <button
            v-if="editing"
            class="btn btn-danger"
            @click="$emit('remove')"
          >
            Remover
          </button>
          <div style="flex: 1" />
          <button class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button class="btn btn-primary" @click="$emit('save')">
            {{ editing ? "Guardar" : "Criar" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modalOpen: { type: Boolean, default: false },
  editing: { type: Object, default: null },
  form: { type: Object, required: true },
  clienteSearch: { type: String, default: "" },
  showSuggestions: { type: Boolean, default: false },
  clienteSuggestions: { type: Array, default: () => [] },
});
defineEmits(["close", "save", "remove", "update:marca", "update:modelo", "update:serie", "update:clienteSearch", "update:showSuggestions", "select-cliente"]);
</script>

<style scoped>
.autocomplete-wrap {
  position: relative;
}
.autocomplete-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 100;
  background: white;
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  margin: 0;
  padding: 0;
  box-shadow: var(--shadow-sm);
}
.autocomplete-list li {
  padding: 8px 12px;
  font-size: 0.875rem;
  cursor: pointer;
  color: var(--text);
}
.autocomplete-list li:hover {
  background: var(--bg);
}
</style>
