<template>
  <div class="card equip-card" @click="$emit('click', equipamento)">
    <div class="equip-header">
      <div class="equip-title">{{ equipamento.marca }} {{ equipamento.modelo }}</div>
      <button
        class="btn-remove"
        title="Remover"
        @click.stop="$emit('remove', equipamento)"
      >✕</button>
    </div>
    <div class="equip-cliente">{{ clienteNome }}</div>
    <div class="equip-details">
      <div class="equip-detail">
        <span class="detail-label">Nº Série</span
        ><span class="serie">{{ equipamento.serie }}</span>
      </div>
    </div>
    <div class="equip-footer">
      <span>Registado em {{ equipamento.registado }}</span>
      <span v-if="equipamento.ultimaManutencao"
        >Última manutenção: {{ equipamento.ultimaManutencao }}</span
      >
    </div>
  </div>
</template>

<script setup>
defineProps({
  equipamento: { type: Object, required: true },
  clienteNome: { type: String, default: "—" },
});
defineEmits(["click", "remove"]);
</script>

<style scoped>
.equip-card {
  padding: 16px;
  cursor: pointer;
  transition: box-shadow var(--transition), transform var(--transition);
}
.equip-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.equip-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}
.equip-title {
  font-weight: 700;
  font-size: 0.95rem;
}
.btn-remove {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  font-size: 0.85rem;
  padding: 2px 5px;
  border-radius: 4px;
  line-height: 1;
  flex-shrink: 0;
}
.btn-remove:hover {
  background: #fee2e2;
  color: #dc2626;
}
.equip-cliente {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 14px;
}
.equip-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
}
.equip-detail {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}
.detail-label {
  color: var(--text-muted);
}
.serie {
  font-family: "DM Mono", monospace;
  font-size: 0.8rem;
}
.equip-footer {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 0.72rem;
  color: var(--text-light);
  padding-top: 12px;
  border-top: 1px solid var(--border);
}
</style>
