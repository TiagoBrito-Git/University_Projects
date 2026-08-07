import { ref } from "vue";
import { API_BASE, authFetch } from "@/api";

export function useUtilizadores() {
  const utilizadores = ref([])
  const loading = ref(false)
  const error = ref(null)

  const API_URL = `${API_BASE}/utilizadores`;

  /**
   * Lista todos os utilizadores
   * GET /utilizadores
   */
  async function fetchUtilizadores() {
    loading.value = true;
    error.value = null;
    try {
      const res = await authFetch(API_URL);
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erro ao carregar utilizadores");
      }
      utilizadores.value = await res.json();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Cria um novo utilizador
   * POST /utilizadores
   * @param {{ nome, username, password, perfil }} data
   */
  async function createUtilizador(data) {
    loading.value = true;
    error.value = null;
    try {
      const res = await authFetch(`${API_URL}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erro ao criar utilizador");
      }
      const created = await res.json();
      utilizadores.value = [...utilizadores.value, created];
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateUtilizador(id, data) {
    loading.value = true;
    error.value = null;
    try {
      const res = await authFetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erro ao editar utilizador");
      }
      const updated = await res.json();
      const idx = utilizadores.value.findIndex(u => u.id === id);
      if (idx !== -1) {
        const next = [...utilizadores.value];
        next[idx] = { ...next[idx], ...updated };
        utilizadores.value = next;
      }
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function desativarUtilizador(id) {
    loading.value = true;
    error.value = null;
    try {
      const res = await authFetch(`${API_URL}/${id}/desativar`, {
        method: "PUT",
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erro ao desativar utilizador");
      }
      utilizadores.value = utilizadores.value.filter(u => u.id !== id);
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    utilizadores,
    loading,
    error,
    fetchUtilizadores,
    createUtilizador,
    updateUtilizador,
    desativarUtilizador,
  };
}