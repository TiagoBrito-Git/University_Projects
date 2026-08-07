<template>
  <div class="search-bar" style="margin-bottom: 20px">
    <span><Search :size="18" /></span>
    <input
      :value="query"
      @input="$emit('update:query', $event.target.value)"
      placeholder="Pesquisar por nome, email, telefone ou NIF..."
    />
  </div>
</template>

<script setup>

import { Search } from "@lucide/vue"
defineProps({
  query: { type: String, default: "" },
});
defineEmits(["update:query"]);
</script>
