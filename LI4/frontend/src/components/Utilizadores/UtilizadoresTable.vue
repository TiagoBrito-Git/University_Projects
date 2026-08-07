<template>
  <div>
    <div v-if="loading" class="empty-state">A carregar utilizadores…</div>
    <div v-else-if="error" class="empty-state" style="color: var(--danger)">
      <TriangleAlert :size="18" /> {{ error }}
    </div>
    <div v-else class="card">
      <div class="table-header">
        <h3>Contas de Utilizador</h3>
      </div>
      <div class="table-wrap">
        <table class="util-table">
          <thead>
            <tr>
              <th>Utilizador</th>
              <th>Username</th>
              <th>Perfil</th>
              <th>Estado</th>
              <th>Registo</th>
              <th v-if="podeGerir" style="width: 100px"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="u in filtered"
              :key="u.id"
              :class="{ 'row-clickable': podeGerir, 'row-inativo': !u.ativo }"
              @click="podeGerir && $emit('open', u)"
            >
              <td>
                <div class="util-info">
                  <div class="util-avatar" :style="{ background: u.ativo ? avatarColor(u.perfil) : '#9ca3af' }">
                    {{ initials(u.nome) }}
                  </div>
                  <div class="util-nome">{{ u.nome }}</div>
                </div>
              </td>
              <td class="util-username">{{ u.username }}</td>
              <td>
                <span class="badge" :class="perfilBadge(u.perfil)">{{ u.perfil }}</span>
              </td>
              <td>
                <span class="badge" :class="u.ativo ? 'badge-success' : 'badge-gray'">
                  {{ u.ativo ? 'Ativo' : 'Desativado' }}
                </span>
              </td>
              <td class="util-data">{{ formatDate(u.data_registo) }}</td>
              <td v-if="podeGerir" class="td-acao" @click.stop>
                <div class="acao-buttons">
                  <button
                    v-if="u.ativo && u.id !== currentUser?.id"
                    class="btn-desativar"
                    :disabled="desativando"
                    @click="$emit('desativar', u, $event)"
                    title="Desativar conta"
                  >
                    Desativar
                  </button>
                  <span class="acao-chevron" @click="$emit('open', u)">›</span>
                </div>
              </td>
            </tr>
            <tr v-if="filtered.length === 0">
              <td :colspan="podeGerir ? 7 : 6" class="empty-row">
                Nenhum utilizador encontrado.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>

import { TriangleAlert } from "@lucide/vue"
import { avatarColor } from "@/helpers"
import { PERFIL_BADGE } from "@/config/utilizadores/constants"

function perfilBadge(p) { return PERFIL_BADGE[p] || "badge-gray" }
defineProps({
  filtered: Array,
  loading: Boolean,
  error: [String, Object],
  podeGerir: Boolean,
  currentUser: Object,
  desativando: Boolean,
})
defineEmits(['open', 'desativar'])

function initials(nome) {
  return nome
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase()
}

function formatDate(d) {
  if (!d) return "—"
  if (typeof d === "string" && d.includes("-")) {
    const [y, m, day] = d.split("-")
    return `${day}/${m}/${y}`
  }
  return d
}
</script>

<style scoped>
.table-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}
.table-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
}
.table-wrap {
  overflow-x: auto;
}
.util-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}
.util-table th {
  text-align: left;
  padding: 10px 16px;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}
.util-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
}
.util-table tr:last-child td {
  border-bottom: none;
}
.util-table tbody tr:hover {
  background: var(--bg);
}
.util-info {
  display: flex;
  align-items: center;
  gap: 10px;
}
.util-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  color: white;
  flex-shrink: 0;
}
.util-nome {
  font-weight: 600;
}
.util-username {
  font-family: "DM Mono", monospace;
  font-size: 0.8rem;
  color: var(--text-muted);
}
.util-data {
  font-size: 0.8rem;
  color: var(--text-muted);
}
.acao-chevron {
  font-size: 1.1rem;
  color: var(--text-muted);
  font-weight: 300;
  line-height: 1;
}
.td-acao {
  text-align: right;
  padding-right: 12px !important;
}
.acao-buttons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}
.btn-desativar {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid #fca5a5;
  background: #fff1f2;
  color: #be123c;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
  white-space: nowrap;
}
.btn-desativar:hover:not(:disabled) {
  background: #ffe4e6;
  border-color: #f87171;
}
.btn-desativar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.row-inativo td {
  opacity: 0.55;
}
.row-inativo .util-nome {
  text-decoration: line-through;
}
.row-clickable {
  cursor: pointer;
  transition: background 0.15s;
}
.row-clickable:hover {
  background: var(--bg) !important;
}
.row-clickable:hover .acao-chevron {
  color: var(--primary);
}
.empty-row {
  text-align: center;
  color: var(--text-muted);
  padding: 32px;
}
.empty-state {
  text-align: center;
  color: var(--text-muted);
  padding: 48px;
  font-size: 0.9rem;
}
</style>
