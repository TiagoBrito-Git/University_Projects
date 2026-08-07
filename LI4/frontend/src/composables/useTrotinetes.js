import { ref } from "vue";
import { API_BASE, authFetch } from "@/api";

export function useTrotinetes() {

  const trotinetes = ref([]);
  const loading = ref(false);
  const error = ref(null);

  async function fetchTrotinetes() {
    loading.value = true;
    error.value = null;

    try {
      const res = await authFetch(`${API_BASE}/trotinetes/`);

      if (!res.ok) {
        throw new Error("Erro ao buscar trotinetes");
      }

      trotinetes.value = await res.json();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  async function createTrotinete(data) {
    try {
      const res = await authFetch(`${API_BASE}/trotinetes/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Erro ao criar trotinete");
      }
      await fetchTrotinetes();
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  }

  async function updateTrotinete(id, data) {
    try {
      const res = await authFetch(`${API_BASE}/trotinetes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Erro ao editar trotinete");
      }
      await fetchTrotinetes();
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  }

  async function deleteTrotinete(id) {
    try {
      const res = await authFetch(`${API_BASE}/trotinetes/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Erro ao remover trotinete");
      }
      await fetchTrotinetes();
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  }

  return {
    trotinetes,
    loading,
    error,
    fetchTrotinetes,
    createTrotinete,
    updateTrotinete,
    deleteTrotinete,
  };
}