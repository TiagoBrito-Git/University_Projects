import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE } from '@/api'
import { STORAGE_KEY } from '@/config/shared/constants'

const currentUser = ref(null)

try {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored) currentUser.value = JSON.parse(stored)
} catch {}

export function useAuth() {
  const router = useRouter()

  async function login(username, password) {
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        return { ok: false, error: data.detail || 'Credenciais inválidas' }
      }

      const data = await res.json()
      // data: { access_token, token_type, perfil, nome }

      const user = {
        name: data.nome,
        perfil: data.perfil,
        token: data.access_token,
      }

      currentUser.value = user
      localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
      return { ok: true }

    } catch {
      return { ok: false, error: 'Não foi possível contactar o servidor.' }
    }
  }

  function logout() {
    currentUser.value = null
    localStorage.removeItem(STORAGE_KEY)
    router.push('/login')
  }

  function authHeaders() {
    const stored = localStorage.getItem(STORAGE_KEY);

    if (!stored) return {};

    const user = JSON.parse(stored);

    return user?.token
      ? { Authorization: `Bearer ${user.token}` }
      : {};
  }

  return { currentUser, login, logout, authHeaders }
}