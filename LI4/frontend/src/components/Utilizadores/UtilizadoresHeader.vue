<template>
  <div class="page-header">
    <div>
      <h1>Utilizadores</h1>
      <p>Gestão de contas e permissões</p>
    </div>
    <button
      v-if="podeGerir"
      class="btn btn-primary"
      @click="$emit('create')"
    >
      + Novo Utilizador
    </button>
  </div>
</template>

<script setup>
defineProps({ podeGerir: Boolean })
defineEmits(['create'])
</script>
