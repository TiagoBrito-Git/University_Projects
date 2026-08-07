<template>
  <div class="card cliente-card" @click="$emit('click')">
    <div class="cliente-header">
      <div class="cliente-avatar">{{ initials(cliente.nome) }}</div>
      <div class="cliente-info">
        <div class="cliente-nome">{{ cliente.nome }}</div>
      </div>
    </div>
    <div class="cliente-details">
      <div class="detail-row"><span><Mail :size="18" /></span> {{ cliente.email }}</div>
      <div class="detail-row"><span><Phone :size="18" /></span> {{ cliente.telefone }}</div>
      <div class="detail-row"><span><MapPin :size="18" /></span> {{ cliente.morada }}</div>
    </div>
  </div>
</template>

<script setup>

import { Mail } from "@lucide/vue"
import { MapPin } from "@lucide/vue"
import { Phone } from "@lucide/vue"
import { initials } from "@/helpers"
defineProps({
  cliente: {
    type: Object,
    required: true,
  },
});
defineEmits(["click"]);
</script>

<style scoped>
.cliente-card {
  padding: 0;
  cursor: pointer;
  transition: box-shadow var(--transition), transform var(--transition);
  overflow: hidden;
}
.cliente-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.cliente-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 16px 12px;
  border-bottom: 1px solid var(--border);
}
.cliente-avatar {
  width: 44px;
  height: 44px;
  background: var(--primary);
  color: #fff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
  flex-shrink: 0;
}
.cliente-info {
  flex: 1;
  min-width: 0;
}
.cliente-nome {
  font-weight: 700;
  font-size: 0.95rem;
}
.cliente-details {
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.detail-row {
  font-size: 0.8rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
