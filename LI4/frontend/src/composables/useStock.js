import { ref } from "vue";
import { setStoreCollection } from "@/store";
import { API_BASE, authFetch } from "@/api";

export function useStock() {

  const pecas = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const API_URL = `${API_BASE}/stock`;

  /**
   * Lista todas as peças
   * Mapeia para o GET /stock no backend
   */
  async function fetchPecas() {
    loading.value = true;
    error.value = null;

    try {
      const res = await authFetch(API_URL);

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Erro ao procurar peças");
      }
      const data = await res.json();
      const mapped = data.map(p => ({
        id: p.codigo,
        nome: p.nome, 
        codigo: p.codigo,          
        descricao: p.descricao,
        categoria:p.categoria,
        fornecedor: p.fornecedor,
        precoUnitario:p.preco,
        stockDisponivel:p.stock,
        stockTotal:p.stock,
        stockMinimo:p.stock_minimo,
        estado: "OK",
      }));
      setStoreCollection("pecas", mapped);
      pecas.value = mapped;
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Cria uma nova peça
   * @param {Object} data - Dados da peça
   */
  async function createPeca(data) {
    loading.value = true;
    error.value = null;
    try {
      const res = await authFetch(`${API_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Erro ao criar ordem de serviço");
      }

      await fetchPecas(); // Refresh da lista
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

// Dentro de useStock.js
async function updatePeca(id, payload) {
  loading.value = true;
  error.value = null;

  try {
    const res = await authFetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Erro ao editar Peca");

    await fetchPecas();

  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
}




  return {
    pecas,
    loading,
    error,
    fetchPecas,
    createPeca,
    updatePeca,
  };
}