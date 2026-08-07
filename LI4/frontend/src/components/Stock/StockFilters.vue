<template>
  <div class="filters-row" style="margin-bottom: 16px">
    <div class="search-bar" style="flex: 1">
      <span><Search :size="18" /></span>
      <input
        :value="query"
        @input="$emit('update:query', $event.target.value)"
        placeholder="Pesquisar por nome, código ou descrição..."
      />
    </div>
    <div class="cat-tabs">
      <button
        v-for="cat in ['Todas', ...categorias]"
        :key="cat"
        class="cat-btn"
        :class="{ active: catFilter === cat }"
        @click="$emit('update:catFilter', cat)"
      >
        {{ cat }}
      </button>
    </div>
  </div>
</template>

<script setup>

import { Search } from "@lucide/vue"
defineProps({
  query: String,
  catFilter: String,
  categorias: Array,
})
defineEmits(['update:query', 'update:catFilter'])
</script>

<style scoped>
.filters-row {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.cat-tabs {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
.cat-btn {
  padding: 6px 14px;
  border-radius: 99px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  border: 1px solid var(--border);
  background: white;
  transition: all var(--transition);
}
.cat-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}
.cat-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}
</style>
