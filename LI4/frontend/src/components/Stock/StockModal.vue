<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ editing ? "Editar Peça" : "Nova Peça" }}</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-row">
          <div class="form-group">
            <label>Nome</label>
            <input v-model="form.nome" class="form-control" />
          </div>
          <div class="form-group">
            <label>Código</label>
            <input v-model="form.codigo" class="form-control" />
          </div>
        </div>
        <div class="form-group">
          <label>Descrição</label>
          <input v-model="form.descricao" class="form-control" />
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Categoria</label>
            <select v-model="form.categoria" class="form-control">
              <option v-for="c in CATEGORIAS" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Fornecedor</label>
            <input v-model="form.fornecedor" class="form-control" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Preço Unitário (€)</label>
            <input
              v-model.number="form.precoUnitario"
              type="number"
              min="0"
              step="0.01"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label>Stock Disponível</label>
            <input
              v-model.number="form.stockDisponivel"
              type="number"
              min="0"
              class="form-control"
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Stock Mínimo</label>
            <input
              v-model.number="form.stockMinimo"
              type="number"
              min="0"
              class="form-control"
            />
          </div>
        </div>
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
          <button class="btn btn-primary" @click="$emit('save')">
            {{ editing ? "Guardar" : "Adicionar" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { CATEGORIAS } from "@/config/stock/constants"
defineProps({
  modalOpen: Boolean,
  editing: Object,
  form: Object,
})
defineEmits(['close', 'save'])
</script>
