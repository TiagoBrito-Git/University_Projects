<template>
  <div class="alert-info">
    <Info :size="18" /> Apenas administradores e gestores podem criar ou editar utilizadores.
  </div>
</template>

<style scoped>
.alert-info {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-left: 3px solid var(--primary);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  font-size: 0.875rem;
  color: #1e40af;
  margin-bottom: 20px;
}
</style>
