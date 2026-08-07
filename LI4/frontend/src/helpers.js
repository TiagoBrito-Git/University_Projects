import { ESTADO_BADGE, ESTADO_COLOR } from "@/config/ordens-servico/constants"
import { AVATAR_COLOR } from "@/config/utilizadores/constants"
import { FATURA_BADGE } from "@/config/faturacao/constants"

export function estadoBadge(e) { return ESTADO_BADGE[e] || "badge-gray" }
export function estadoColor(e) { return ESTADO_COLOR[e] || "#f3f4f6" }
export function avatarColor(p) { return AVATAR_COLOR[p] || "#6b7280" }
export function faturaBadge(e) { return FATURA_BADGE[e] || "badge-gray" }

export function initials(nome) {
  return (nome || "")
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase()
}

export function isVencida(f) {
  if (f.estado === "Paga") return false
  if (!f.vencimento) return false
  const [d, m, y] = f.vencimento.split("/").map(Number)
  return new Date(y, m - 1, d) < new Date()
}

export function tipoBadge(tipo) {
  const m = {
    Económico: "badge-success",
    Stock: "badge-info",
    Performance: "badge-warning",
  }
  return m[tipo] || "badge-gray"
}
