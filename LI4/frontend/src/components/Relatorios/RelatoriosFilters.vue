<template>
  <div
    style="
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      align-items: center;
      flex-wrap: wrap;
    "
  >
    <div class="search-bar" style="flex: 1; min-width: 200px">
      <span><Search :size="18" /></span>
      <input
        :value="query"
        @input="$emit('update:query', $event.target.value)"
        placeholder="Pesquisar por nome de relatório..."
      />
    </div>
    <div class="estado-tabs">
      <button
        v-for="t in tipoTabs"
        :key="t"
        class="etab"
        :class="{ active: tabFilter === t }"
        @click="$emit('update:tabFilter', t)"
      >
        {{ t }}
      </button>
    </div>
  </div>
</template>

<script setup>

import { Search } from "@lucide/vue"
defineProps({
  query: { type: String, required: true },
  tabFilter: { type: String, required: true },
  tipoTabs: { type: Array, required: true },
})

defineEmits(['update:query', 'update:tabFilter'])
</script>

<style scoped>
.estado-tabs {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
.etab {
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  border: 1px solid var(--border);
  background: white;
  transition: all var(--transition);
}
.etab:hover {
  border-color: var(--primary);
  color: var(--primary);
}
.etab.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}
</style>
