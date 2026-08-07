<template>
  <div class="filters-row" style="margin-bottom: 16px">
    <div class="search-bar" style="flex: 1">
      <span><Search :size="18" /></span>
      <input :value="query" @input="$emit('update:query', $event.target.value)" placeholder="Pesquisar por nome ou username..." />
    </div>
    <div class="filter-select-wrap">
      <select :value="perfilFilter" @change="$emit('update:perfilFilter', $event.target.value)" class="filter-select">
        <option value="">Todos os perfis</option>
        <option v-for="p in PERFIS" :key="p">{{ p }}</option>
      </select>
    </div>
  </div>
</template>

<script setup>

import { Search } from "@lucide/vue"
import { PERFIS } from "@/config/utilizadores/constants"
defineProps({ query: String, perfilFilter: String })
defineEmits(['update:query', 'update:perfilFilter'])
</script>

<style scoped>
.filters-row {
  display: flex;
  gap: 12px;
  align-items: center;
}
.filter-select-wrap {
  position: relative;
}
.filter-select {
  appearance: none;
  background: white
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M6 8L1 3h10z'/%3E%3C/svg%3E")
    no-repeat right 10px center;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 8px 32px 8px 12px;
  font-size: 0.875rem;
  outline: none;
  cursor: pointer;
  color: var(--text);
  min-width: 180px;
}
.filter-select:focus {
  border-color: var(--primary);
}
</style>
