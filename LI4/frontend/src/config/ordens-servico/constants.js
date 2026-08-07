export const TAB_ESTADOS = {
  diagnostico: "Aguarda Diagnóstico",
  resposta: "Aguarda Resposta",
  reparacao: "Em Reparação",
  faturacao: "Aguarda Faturação",
  concluido: "Concluído",
  faturada: "Faturada",
  encerrada: "Encerrada",
  cancelada: "Cancelada",
}

export const ESTADOS_OS = Object.values(TAB_ESTADOS)

export const ESTADOS_FINAIS = ["Concluído", "Faturada", "Encerrada", "Cancelada"]

export const LABEL_AVANCAR = {
  "Aguarda Diagnóstico": "Aguarda Resposta",
  "Em Reparação": "Aguarda Faturação",
}

export const ESTADO_BADGE = {
  "Aguarda Diagnóstico": "badge-warning",
  "Aguarda Resposta": "badge-info",
  "Em Reparação": "badge-purple",
  "Aguarda Faturação": "badge-danger",
  Concluído: "badge-success",
  Faturada: "badge-success",
  Encerrada: "badge-gray",
  Cancelada: "badge-gray",
}

export const ESTADO_COLOR = {
  "Aguarda Diagnóstico": "#fef3c7",
  "Aguarda Resposta": "#dbeafe",
  "Em Reparação": "#ede9fe",
  "Aguarda Faturação": "#fee2e2",
  Concluído: "#dcfce7",
  Faturada: "#dcfce7",
  Encerrada: "#f3f4f6",
  Cancelada: "#f3f4f6",
}
