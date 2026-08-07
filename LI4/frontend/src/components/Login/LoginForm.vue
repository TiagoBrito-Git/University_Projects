<template>
  <form class="login-form" @submit.prevent="handleLogin">
    <div class="form-group">
      <label>Username</label>
      <input v-model="username" type="text" class="form-control" placeholder="username" autocomplete="username" />
    </div>
    <div class="form-group" v-if="username">
      <label>Password</label>
      <input v-model="password" type="password" class="form-control" placeholder="••••••••" autocomplete="current-password" />
    </div>
    <div class="error-msg" v-if="error">{{ error }}</div>
    <button type="submit" class="btn btn-primary login-btn" :disabled="loading">
      <span v-if="loading">A entrar…</span>
      <span v-else>Entrar</span>
    </button>
  </form>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const { login } = useAuth()
const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

async function handleLogin() {
  error.value = ""
  if (!username.value) return
  loading.value = true
  const result = await login(username.value, password.value)
  loading.value = false
  if (result.ok) {
    router.push("/dashboard")
  } else {
    error.value = result.error || "Credenciais inválidas."
  }
}
</script>

<style scoped>
.login-form { text-align: left; position: relative; }
.form-group { margin-bottom: 16px; position: relative; }
.form-group label { display: block; font-size: 0.8rem; font-weight: 600; color: var(--text-muted); margin-bottom: 5px; }
.error-msg { background: var(--danger-bg); color: var(--danger); padding: 8px 12px; border-radius: var(--radius-sm); font-size: 0.85rem; margin-bottom: 14px; }
.login-btn { width: 100%; justify-content: center; padding: 12px; font-size: 0.95rem; margin-top: 4px; }
.login-btn:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
