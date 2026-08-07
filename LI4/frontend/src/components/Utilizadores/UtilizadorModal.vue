<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <div v-if="editing" class="modal-header-user">
          <div class="modal-avatar" :style="{ background: avatarColor(editing.perfil) }">
            {{ initials(editing.nome) }}
          </div>
          <div>
            <h2>Editar Utilizador</h2>
            <span class="modal-username-label">{{ editing.username }}</span>
          </div>
        </div>
        <h2 v-else>Novo Utilizador</h2>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Nome completo <span class="required">*</span></label>
          <input v-model="form.nome" class="form-control" placeholder="Ex: João Silva" />
        </div>
        <div class="form-group" v-if="!editing">
          <label>Username (email) <span class="required">*</span></label>
          <input
            v-model="form.username"
            class="form-control"
            type="email"
            placeholder="joao.silva@oficina.pt"
          />
        </div>
        <div class="form-group">
          <label>Perfil <span class="required">*</span></label>
          <select v-model="form.perfil" class="form-control">
            <option
              v-for="p in PERFIS"
              :key="p"
              :value="p"
              v-show="p === 'secretaria' || p === 'tecnico' || currentUser?.perfil === 'administrador'"
            >{{ p.charAt(0).toUpperCase() + p.slice(1) }}</option>
          </select>
          <div class="form-hint">{{ permissoesLabel(form.perfil) }}</div>
        </div>
        <div class="form-group">
          <label>
            Password
            <span class="required" v-if="!editing">*</span>
            <span class="optional" v-else>(deixar em branco para não alterar)</span>
          </label>
          <div class="password-wrap">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-control"
              placeholder="Mínimo 8 caracteres, 1 maiúscula, 1 número"
            />
            <button class="toggle-pw" type="button" @click="showPassword = !showPassword">
              <EyeOff :size="18" v-if="showPassword" /><Eye :size="18" v-else />
            </button>
          </div>
          <div class="pw-strength" v-if="form.password">
            <div class="pw-bar">
              <div
                class="pw-fill"
                :style="{ width: passwordStrength.pct + '%', background: passwordStrength.color }"
              ></div>
            </div>
            <span :style="{ color: passwordStrength.color }">{{ passwordStrength.label }}</span>
          </div>
        </div>
        <div class="alert-erro" v-if="formError"><TriangleAlert :size="18" /> {{ formError }}</div>
        <div class="modal-footer">
          <button
            v-if="editing && editing.ativo && editing.id !== currentUser?.id"
            class="btn btn-danger"
            :disabled="desativando"
            @click="$emit('desativar', editing)"
          >
            {{ desativando ? 'A desativar…' : 'Desativar conta' }}
          </button>
          <div style="flex:1" />
          <button class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button class="btn btn-primary" :disabled="saving" @click="saveUtilizador">
            <span v-if="saving">A guardar…</span>
            <span v-else>{{ editing ? "Guardar alterações" : "Criar utilizador" }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { Eye } from "@lucide/vue"
import { EyeOff } from "@lucide/vue"
import { TriangleAlert } from "@lucide/vue"
import { avatarColor, initials } from "@/helpers"
import { PERFIS, PERMISSOES_LABEL } from "@/config/utilizadores/constants"

function permissoesLabel(p) { return PERMISSOES_LABEL[p] || "" }
import { ref, reactive, computed, watch } from "vue"
import { useUtilizadores } from "@/composables/useUtilizadores"
import { useToast } from "@/composables/useToast"

const { createUtilizador, updateUtilizador } = useUtilizadores()
const { toast } = useToast()

const props = defineProps({
  modalOpen: Boolean,
  editing: Object,
  currentUser: Object,
  desativando: Boolean,
})
const emit = defineEmits(["close", "save", "desativar"])

const showPassword = ref(false)
const saving = ref(false)
const formError = ref("")

const form = reactive({
  nome: "",
  username: "",
  perfil: "tecnico",
  password: "",
})

watch(() => props.modalOpen, (open) => {
  if (!open) return
  const u = props.editing
  formError.value = ""
  showPassword.value = false
  if (u) {
    form.nome = u.nome
    form.username = u.username
    form.perfil = u.perfil
    form.password = ""
  } else {
    form.nome = ""
    form.username = ""
    form.perfil = "tecnico"
    form.password = ""
  }
})

const passwordStrength = computed(() => {
  const pw = form.password
  if (!pw) return { pct: 0, label: "", color: "" }
  let score = 0
  if (pw.length >= 8) score++
  if (pw.length >= 12) score++
  if (/[A-Z]/.test(pw)) score++
  if (/[0-9]/.test(pw)) score++
  if (/[^A-Za-z0-9]/.test(pw)) score++
  const levels = [
    { pct: 20, label: "Muito fraca", color: "#ef4444" },
    { pct: 40, label: "Fraca", color: "#f97316" },
    { pct: 60, label: "Razoável", color: "#f59e0b" },
    { pct: 80, label: "Boa", color: "#22c55e" },
    { pct: 100, label: "Excelente", color: "#16a34a" },
  ]
  return levels[Math.min(score - 1, 4)] ?? levels[0]
})

function validarForm() {
  if (!form.nome.trim()) return "O nome é obrigatório."
  if (!props.editing && !form.username.trim()) return "O username é obrigatório."
  if (!props.editing || form.password) {
    if (form.password.length < 8) return "A password deve ter pelo menos 8 caracteres."
    if (!/[A-Z]/.test(form.password)) return "A password deve ter pelo menos 1 letra maiúscula."
    if (!/[0-9]/.test(form.password)) return "A password deve ter pelo menos 1 número."
  }
  return null
}

async function saveUtilizador() {
  formError.value = ""
  const erro = validarForm()
  if (erro) {
    formError.value = erro
    return
  }
  saving.value = true
  try {
    const payload = { nome: form.nome, perfil: form.perfil }
    if (form.password) payload.password = form.password
    if (props.editing) {
      payload.id = props.editing.id
      const { id, ...data } = payload
      await updateUtilizador(id, data)
    } else {
      payload.username = form.username
      await createUtilizador(payload)
    }
    saving.value = false
    emit("close")
    toast(props.editing ? "Utilizador atualizado com sucesso!" : "Utilizador criado com sucesso!", "success")
  } catch (err) {
    formError.value = err.message
    toast(err.message)
    saving.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}
.modal {
  background: white;
  border-radius: var(--radius, 12px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modal-in 0.18s ease;
}
@keyframes modal-in {
  from { opacity: 0; transform: translateY(12px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0)   scale(1);    }
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid var(--border);
}
.modal-header h2 {
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
}
.modal-close {
  background: none;
  border: none;
  font-size: 1.1rem;
  cursor: pointer;
  color: var(--text-muted);
  padding: 4px 6px;
  border-radius: 6px;
  line-height: 1;
  transition: background 0.15s;
}
.modal-close:hover {
  background: var(--bg);
}
.modal-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.modal-header-user {
  display: flex;
  align-items: center;
  gap: 12px;
}
.modal-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  color: white;
  flex-shrink: 0;
}
.modal-username-label {
  font-size: 0.78rem;
  color: var(--text-muted);
  font-family: "DM Mono", monospace;
}
.modal-footer {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
}
.form-control {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm, 8px);
  padding: 9px 12px;
  font-size: 0.875rem;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.15s;
}
.form-control:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(26, 86, 219, 0.1);
}
.required {
  color: var(--danger);
}
.optional {
  font-weight: 400;
  color: var(--text-muted);
  font-size: 0.78rem;
  margin-left: 4px;
}
.form-hint {
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 4px;
  font-style: italic;
}
.password-wrap {
  position: relative;
}
.password-wrap .form-control {
  padding-right: 40px;
}
.toggle-pw {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1rem;
  color: var(--text-muted);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}
.pw-strength {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}
.pw-bar {
  flex: 1;
  height: 4px;
  background: #e5e7eb;
  border-radius: 99px;
  overflow: hidden;
}
.pw-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.3s ease, background 0.3s ease;
}
.pw-strength span {
  font-size: 0.72rem;
  font-weight: 600;
  white-space: nowrap;
}
.alert-erro {
  margin-top: 10px;
  padding: 10px 14px;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-left: 3px solid var(--danger);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: #be123c;
}
</style>
