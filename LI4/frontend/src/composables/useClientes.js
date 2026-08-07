import { ref } from "vue";
import { setStoreCollection, getStoreCollection } from "@/store";
import { API_BASE, authFetch } from "@/api";
import { useToast } from "./useToast";

export function useClientes() {
  const { toast } = useToast();

  const clientes = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const API_URL = `${API_BASE}/clientes`;

  async function fetchClientes() {
    loading.value = true;
    error.value = null;

    try {
      const res = await authFetch(`${API_URL}/`);

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Erro ao procurar clientes");
      }
      const data = await res.json();
        const mapped = data.map(cliente => ({
        id: cliente.id,
        nome: cliente.nome,
        email: cliente.email,
        telefone: cliente.contacto,
        morada: cliente.morada,
        nif: cliente.nif,
        desde: cliente.desde || "N/A", 
        equipamentos: cliente.equipamentos || 0,
        totalGasto: cliente.totalGasto || 0
        }));
      setStoreCollection("clientes", mapped);
      clientes.value = data;

    } catch (err) {
      error.value = err.message;
      toast(err.message);
    } finally {
      loading.value = false;
    }
  }

    async function createCliente(data) {
    loading.value = true;
    try {
        const res = await authFetch(`${API_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        });

        if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "Erro ao criar cliente");
        }

        await fetchClientes();
    } catch (err) {
        error.value = err.message;
        throw err;
    } finally {
        loading.value = false;
    }
    }

    async function updateCliente(id, data) {
    loading.value = true;
    try {
        const res = await authFetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        });

        if (!res.ok) {
          const errorData = await res.json();
          throw new Error(errorData.detail || "Erro ao editar cliente");
        }
        await fetchClientes();
    } catch (err) {
        error.value = err.message;
        throw err;
    } finally {
        loading.value = false;
    }
    }

    async function deleteCliente(id) {
    if (!confirm(`Deseja remover o cliente com ID ${id}?`)) return;

    loading.value = true;
    try {
        const res = await authFetch(`${API_URL}/${id}`, {
        method: "DELETE",
        });

        if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Erro ao remover cliente");
        }

        await fetchClientes();
    } catch (err) {
        error.value = err.message;
        toast(err.message);
    } finally {
        loading.value = false;
    }
    }


  return {
    clientes,
    loading,
    error,
    fetchClientes,
    updateCliente,
    createCliente,
    deleteCliente,
  };
}