<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ editing ? "Editar Cliente" : "Novo Cliente" }}</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-row">
          <div class="form-group">
            <label>Nome</label>
            <input
              :value="form.nome"
              @input="$emit('update:form', { ...form, nome: $event.target.value })"
              class="form-control"
              placeholder="Nome completo"
            />
          </div>
          <div class="form-group">
            <label>NIF</label>
            <input
              :value="form.nif"
              @input="$emit('update:form', { ...form, nif: $event.target.value })"
              class="form-control"
              placeholder="123456789"
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Email</label>
            <input
              :value="form.email"
              @input="$emit('update:form', { ...form, email: $event.target.value })"
              class="form-control"
              type="email"
            />
          </div>
          <div class="form-group">
            <label>Telefone</label>
            <input
              :value="form.telefone"
              @input="$emit('update:form', { ...form, telefone: $event.target.value })"
              class="form-control"
              placeholder="9XXXXXXXX"
            />
          </div>
        </div>
        <div class="form-group">
          <label>Morada</label>
          <input
            :value="form.morada"
            @input="$emit('update:form', { ...form, morada: $event.target.value })"
            class="form-control"
            placeholder="Rua, Nº, Cidade"
          />
        </div>
        <div
          style="
            display: flex;
            gap: 8px;
            justify-content: flex-end;
            margin-top: 8px;
          "
        >
          <button
            v-if="editing"
            class="btn btn-danger"
            style="margin-right: auto; background-color: #dc3545; color: white;"
            @click="$emit('delete')"
          >
            Eliminar
          </button>
          <button class="btn btn-secondary" @click="$emit('close')">
            Cancelar
          </button>
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
});
defineEmits(["close", "save", "delete", "update:form"]);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
.modal {
  background: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 540px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  overflow: hidden;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
}
.modal-header h2 {
  margin: 0;
  font-size: 1.2rem;
}
.modal-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--text-muted);
}
.modal-body {
  padding: 20px 24px 24px;
}
.form-row {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}
.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.form-group label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.form-control {
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color var(--transition);
}
.form-control:focus {
  border-color: var(--primary);
}
</style>
