<template>
  <div class="page-header">
    <div>
      <h1>Faturação</h1>
      <p>Gestão de faturas e pagamentos</p>
    </div>
    <button class="btn btn-primary" @click="$emit('create')">+ Nova Fatura</button>
  </div>
</template>

<script setup>
defineEmits(['create'])
</script>
