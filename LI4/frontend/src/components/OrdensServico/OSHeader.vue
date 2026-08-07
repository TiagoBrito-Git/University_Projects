<template>
  <div class="page-header">
    <div>
      <h1>Ordens de Serviço</h1>
      <p>Gestão e acompanhamento de serviços</p>
    </div>
    <button class="btn btn-primary" @click="$emit('create')">+ Nova Ordem</button>
  </div>
</template>

<script setup>
defineEmits(["create"]);
</script>
