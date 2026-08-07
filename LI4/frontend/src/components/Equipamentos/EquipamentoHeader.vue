<template>
  <div class="page-header">
    <div>
      <h1>Equipamentos</h1>
      <p>Gestão de trotinetes e equipamentos</p>
    </div>
    <button class="btn btn-primary" @click="$emit('create')">
      + Novo Equipamento
    </button>
  </div>
</template>

<script setup>
defineEmits(["create"]);
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}
.page-header p {
  color: var(--text-muted);
  font-size: 0.875rem;
  margin: 4px 0 0 0;
}
</style>
