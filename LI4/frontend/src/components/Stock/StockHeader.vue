<template>
  <div class="page-header">
    <div>
      <h1>Stock & Peças</h1>
      <p>Gestão de inventário e peças</p>
    </div>
    <button class="btn btn-primary" @click="$emit('create')">
      + Adicionar Peça
    </button>
  </div>
</template>

<script setup>
defineEmits(['create'])
</script>
