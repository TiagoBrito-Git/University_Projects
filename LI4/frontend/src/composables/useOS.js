import { ref } from "vue";
import { setStoreCollection } from "@/store";
import { API_BASE, authFetch } from "@/api";
import { DEFAULT_TAXA_MAO_OBRA, DEFAULT_TAXA_DIAGNOSTICO } from "@/config/shared/constants";

export function useOS() {
  const ordemSelecionada = ref(null);
  const ordens = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const API_URL = `${API_BASE}/os`;

  /**
   * Lista todas as Ordens de Serviço
   * Mapeia para o GET /os no backend
   */
  async function fetchOrdens() {
    loading.value = true;
    error.value = null;

    try {
      const res = await authFetch(`${API_URL}/`);

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Erro ao procurar ordens de serviço");
      }
      const data = await res.json();
      const mapped = data.map(os => ({
        id: os.id,
        titulo: os.descricao,           // ou adicionar titulo ao backend
        descricao: os.descricao,
        estado: os.estado,
        clienteId: null,                // não vem do backend
        clienteNome: os.nome_cliente,   // usar diretamente
        clienteEmail: os.email_cliente,
        equipamentoId: null,
        equipamentoNome: os.trotinete,
        numeroSerie: os.numero_serie,
        tecnico: os.tecnico,
        abertura: os.data_abertura,
        valorEstimado: 0,
        diagnostico: os.diagnostico ? {
          descricao: os.diagnostico.descricao,
          tempo_estimado: os.diagnostico.tempo_estimado,
          pecas: os.diagnostico.pecas || [] // Lista de peças do diagnóstico
        } : null,
        intervencoes: os.intervencoes || [],
      }));
      setStoreCollection("ordensServico", mapped);
      ordens.value = data;
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Cria uma nova Ordem de Serviço
   * @param {Object} data - Objeto contendo descricao, nif_cliente, n_serie_trotinete, id_tecnico
   */
  async function createOrdem(data) {
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

      await fetchOrdens(); // Refresh da lista
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Edita uma Ordem de Serviço existente
   * Nota: O endpoint no backend (os_router.py) estava definido como /os/trotinetes/{id} 
   * mas o schema OSALTER espera id, data_conclusao, etc.
   */
  async function updateOrdem(data) {
    loading.value = true;
    error.value = null;
    try {
      const res = await authFetch(`${API_URL}/${data.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Erro ao editar ordem de serviço");
      }

      await fetchOrdens();
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

    async function registarIntervencao(id,data) {
      loading.value = true;
      try {
          const res = await authFetch(`${API_URL}/${id}/intervencao`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
          });

          if (!res.ok) {
          const errorData = await res.json();
          throw new Error(errorData.detail || "Erro ao mudar estado");
          }

          await fetchOrdens();
      } catch (err) {
          error.value = err.message;
          throw err;
      } finally {
          loading.value = false;
      }
    }

    async function registarDiagnostico(id,data) {
      loading.value = true;
      try {
          const res = await authFetch(`${API_URL}/${id}/diagnostico`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
          });

          if (!res.ok) {
          const errorData = await res.json();
          throw new Error(errorData.detail || "Erro ao mudar estado");
          }

          await fetchOrdens();
      } catch (err) {
          error.value = err.message;
          throw err;
      } finally {
          loading.value = false;
      }
    }




    
async function avancarProximoEstado(id) {
  loading.value = true;
  try {
    const res = await authFetch(`${API_URL}/${id}/avancar`, {
      method: "PUT",
    });
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Erro ao avançar estado");
    }
    await fetchOrdens();
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
}

async function fetchConfig() {
  try {
    const res = await authFetch(`${API_URL}/config`);
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return { taxa_mao_obra: DEFAULT_TAXA_MAO_OBRA, taxa_diagnostico: DEFAULT_TAXA_DIAGNOSTICO };
  }
}

async function finalizarOS(id, estado) {
  loading.value = true;
  error.value = null;
  try {
    const res = await authFetch(`${API_URL}/${id}/resposta`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, estado }),
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Erro ao finalizar OS");
    }

    await fetchOrdens();
    return { success: true };
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
}




async function registarDecisaoCliente(id, decisao) {
  loading.value = true;
  try {
    const res = await authFetch(`${API_URL}/${id}/decisao-cliente`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decisao }),
    });
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Erro ao registar decisão do cliente");
    }
    await fetchOrdens();
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
}

async function pagarFatura(id_fatura) {
  loading.value = true;
  try {
    const res = await authFetch(`${API_BASE}/fatura/${id_fatura}/pagar`, {
      method: "PUT",
    });
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Erro ao pagar fatura");
    }
    await fetchOrdens();
  } catch (err) {
    error.value = err.message;
    throw err;
  } finally {
    loading.value = false;
  }
}

async function fetchDetalhesOS(id) {
  loading.value = true;
  error.value = null;
  try {
    const res = await authFetch(`${API_URL}/${id}/detalhes`);

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Erro ao obter detalhes da OS");
    }

    const dados = await res.json();

    // Mapear a resposta do backend para o formato que a view espera
    ordemSelecionada.value = {
      id: dados.id,
      descricao: dados.descricao,
      estado: dados.estado,
      clienteNome: dados.nome_cliente ?? "",
      clienteEmail: dados.email_cliente ?? "",
      equipamentoNome: dados.trotinete ?? "",
      numeroSerie: dados.numero_serie ?? "",
      tecnico: dados.tecnico ?? "",
      abertura: dados.data_abertura,

      diagnostico: dados.diagnostico ? {
        descricao: dados.diagnostico.descricao,
        horas_estimadas: dados.diagnostico.horas_mao_de_obra,
        orcamento_estimado: dados.diagnostico.orcamento_estimado,
        data: dados.diagnostico.data,
        pecas: dados.diagnostico.pecas ?? [],
      } : null,

      intervencoes: (dados.intervencoes ?? []).map(i => ({
        id: i.id,
        descricao: i.descricao,
        horas: i.horas_trabalhadas,
        data: i.data,
        id_tecnico: i.id_tecnico,
        custo: i.custo_total,
        pecas: i.pecas_usadas ?? [],
      })),
    };

    return ordemSelecionada.value;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}


  return {
    ordemSelecionada,
    ordens,
    loading,
    error,
    fetchOrdens,
    fetchDetalhesOS,
    createOrdem,
    updateOrdem,
    avancarProximoEstado,
    fetchConfig,
    registarIntervencao,
    registarDiagnostico,
    finalizarOS,
    registarDecisaoCliente,
    pagarFatura,
  };
}