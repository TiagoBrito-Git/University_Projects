import { ref } from "vue";
import { setStoreCollection } from "@/store";
import { API_BASE, authFetch } from "@/api";
import { useToast } from "./useToast";

export function useRelatorios() {
  const { toast } = useToast();
  const relatorios = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const API_URL = `${API_BASE}/relatorios`;

  async function fetchRelatorios() {
    loading.value = true;
    error.value = null;
    try {
      const res = await authFetch(`${API_URL}/`);
      if (!res.ok) throw new Error("Erro ao carregar relatórios");
      relatorios.value = await res.json();
    } catch (e) {
      error.value = e.message;
      toast(e.message);
    } finally {
      loading.value = false;
    }
  }

  async function downloadRelatorioPDF(id, nomeArquivo) {
    try {
      const res = await authFetch(`${API_URL}/${id}/download`);
      if (!res.ok) throw new Error("Ficheiro não encontrado no servidor");
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", nomeArquivo || `relatorio_${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      error.value = e.message;
      toast(e.message);
    }
  }

  return {
    relatorios,
    loading,
    error,
    fetchRelatorios,
    downloadRelatorioPDF,
  };
}