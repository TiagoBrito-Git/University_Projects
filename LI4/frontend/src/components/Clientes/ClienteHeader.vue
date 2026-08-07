<template>
  <div class="page-header">
    <div>
      <h1>Clientes</h1>
      <p>Gestão de clientes da oficina</p>
    </div>
    <button class="btn btn-primary" @click="$emit('create')">
      + Novo Cliente
    </button>
  </div>
</template>

<script setup>
defineEmits(["create"]);
</script>
