import { ref } from "vue";
import { setStoreCollection, getStoreCollection } from "@/store";
import { API_BASE, authFetch } from "@/api";
import { BACKEND_ESTADO_MAP } from "@/config/faturacao/constants";
import { useToast } from "./useToast";

export function useFaturacao() {
  const { toast } = useToast();
  const loading = ref(false);
  const error = ref(null);

  const API_URL = `${API_BASE}/fatura`;

  // useFaturacao.js
  async function fetchFaturas() {
    loading.value = true;
    try {
      const res = await authFetch(`${API_URL}/`);
      if (!res.ok) throw new Error("Erro ao carregar faturas");
      const data = await res.json();

      setStoreCollection("faturas", data.map(f => {
        const subtotal = (f.sub_total_pecas ?? 0) + (f.sub_total_mao_obra ?? 0);
        return {
          id:            f.id,
          numero:        f.numero,
          emissao:       f.data,
          vencimento:    f.data,
          estado:        BACKEND_ESTADO_MAP[f.estado] ?? f.estado,
          subtotal:      subtotal,
          total:         f.total ?? subtotal,
          clienteId:     null,
          nomeCliente:   f.nome_cliente  ?? null,
          nifCliente:    f.nif_cliente   ?? null,
          emailCliente:  f.email_cliente ?? null,
          moradaCliente: f.morada_cliente ?? null,
          ordemId:       f.id_os,
          itens: f.pecas.map(p => ({
            descricao: p.nome,
            qty:       p.quantidade,
            preco:     p.preco_unitario,
            total:     p.subtotal ?? p.quantidade * p.preco_unitario,
          })),
        };
      }));
    } catch (err) {
      error.value = err.message;
      toast(err.message);
    } finally {
      loading.value = false;
    }
  }

  async function downloadFaturaPDF(idFatura, numeroFatura) {
    try {
      const res = await authFetch(`${API_URL}/${idFatura}/download`);
      
      if (!res.ok) throw new Error("Erro ao descarregar PDF");

      // Converte a resposta em Blob (Binary Large Object)
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      
      // Cria um link temporário para forçar o download
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `fatura_${numeroFatura}.pdf`);
      document.body.appendChild(link);
      link.click();
      
      // Limpeza
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      toast(err.message);
    }
  }

  async function pagarFatura(idFatura) {
    try {
      const res = await authFetch(`${API_URL}/${idFatura}/pagar`, {
        method: "PUT",
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "Erro ao pagar fatura");
      }
      const faturas = getStoreCollection("faturas").map(f =>
        f.id === idFatura ? { ...f, estado: "Paga" } : f
      );
      setStoreCollection("faturas", faturas);
    } catch (err) {
      toast(err.message);
      throw err;
    }
  }

  return {
    loading,
    error,
    fetchFaturas,
    downloadFaturaPDF,
    pagarFatura,
  };
}