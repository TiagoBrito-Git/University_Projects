<template>
  <div class="filters-row">
    <div class="search-bar" style="flex: 1">
      <span><Search :size="18" /></span>
      <input :value="query" @input="$emit('update:query', $event.target.value)" placeholder="Pesquisar ordens de serviço..." />
    </div>
    <select :value="estadoFilter" @change="$emit('update:estadoFilter', $event.target.value)" class="filter-select">
      <option value="">Todos os estados</option>
      <option v-for="e in ESTADOS_OS" :key="e">{{ e }}</option>
    </select>
  </div>

  <div class="tabs">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      class="tab-btn"
      :class="{ active: activeTab === tab.key }"
      @click="$emit('update:activeTab', tab.key)"
    >
      {{ tab.label }} ({{ tab.count }})
    </button>
  </div>
</template>

<script setup>

import { Search } from "@lucide/vue"
import { ESTADOS_OS } from "@/config/ordens-servico/constants"
defineProps({
  query: { type: String, default: "" },
  estadoFilter: { type: String, default: "" },
  activeTab: { type: String, default: "all" },
  tabs: { type: Array, default: () => [] },
});

defineEmits(["update:query", "update:estadoFilter", "update:activeTab"]);
</script>

<style scoped>
.filters-row {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  align-items: center;
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
  min-width: 160px;
}
.tabs {
  display: flex;
  gap: 2px;
  overflow-x: auto;
  margin-bottom: 16px;
  background: var(--bg);
  border-radius: var(--radius-sm);
  padding: 4px;
}
.tab-btn {
  padding: 7px 14px;
  border-radius: calc(var(--radius-sm) - 2px);
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
  transition: background var(--transition), color var(--transition);
}
.tab-btn:hover {
  background: white;
  color: var(--text);
}
.tab-btn.active {
  background: white;
  color: var(--primary);
  box-shadow: var(--shadow);
}
</style>
