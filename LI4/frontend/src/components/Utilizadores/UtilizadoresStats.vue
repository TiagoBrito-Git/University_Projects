<template>
  <div class="stats-row" style="margin-bottom: 20px">
    <div class="stat-card" v-for="stat in perfilStats" :key="stat.label">
      <div class="label">{{ stat.label }}</div>
      <div class="value">{{ stat.count }}</div>
      <div class="icon"><component :is="stat.icon" :size="24" /></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Crown, BarChart3, Wrench, ClipboardList } from "@lucide/vue";

const props = defineProps({
  utilizadores: { type: Array, required: true },
})

const perfilStats = computed(() => [
  {
    label: "Administradores",
    icon: Crown,
    count: props.utilizadores.filter((u) => u.perfil === "administrador").length,
  },
  {
    label: "Gestores",
    icon: BarChart3,
    count: props.utilizadores.filter((u) => u.perfil === "gestor").length,
  },
  {
    label: "Técnicos",
    icon: Wrench,
    count: props.utilizadores.filter((u) => u.perfil === "tecnico").length,
  },
  {
    label: "Secretaria",
    icon: ClipboardList,
    count: props.utilizadores.filter((u) => u.perfil === "secretaria").length,
  },
])
</script>
