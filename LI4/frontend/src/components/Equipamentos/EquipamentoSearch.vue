<template>
  <div class="search-bar" style="flex: 1">
    <span><Search :size="18" /></span>
    <input
      :value="query"
      @input="$emit('update:query', $event.target.value)"
      placeholder="Pesquisar por marca, modelo ou nº série..."
    />
  </div>
</template>

<script setup>

import { Search } from "@lucide/vue"
defineProps({ query: { type: String, default: "" } });
defineEmits(["update:query"]);
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  transition: border-color var(--transition);
}
.search-bar:focus-within {
  border-color: var(--primary);
}
.search-bar input {
  border: none;
  background: none;
  outline: none;
  font-size: 0.875rem;
  width: 100%;
  color: var(--text);
}
</style>
