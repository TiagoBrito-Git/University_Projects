<template>
  <div class="card peca-card" @click="$emit('click')">
    <div class="peca-header">
      <div>
        <div class="peca-nome">{{ peca.nome }}</div>
        <div class="peca-codigo">{{ peca.codigo }}</div>
      </div>
      <span class="badge" :class="estadoBadge(peca.estado)">{{
        peca.estado
      }}</span>
    </div>
    <div class="peca-desc">{{ peca.descricao }}</div>
    <div class="peca-stock">
      <div class="stock-nums">
        <span>Stock disponível</span>
        <strong>{{ peca.stockDisponivel }} unidades</strong>
      </div>
      <div class="stock-bar">
        <div
          class="stock-bar-fill"
          :style="{
            width: stockPercent(peca) + '%',
            background: stockColor(peca),
          }"
        ></div>
      </div>
      <div class="stock-min-label">
        Mínimo: {{ peca.stockMinimo }} unidades
      </div>
    </div>
    <div class="peca-meta">
      <div>
        <div class="meta-label">Categoria</div>
        <div class="meta-value">{{ peca.categoria }}</div>
      </div>
      <div>
        <div class="meta-label">Fornecedor</div>
        <div class="meta-value">{{ peca.fornecedor }}</div>
      </div>
    </div>
    <div class="peca-footer">
      <div>
        <div class="meta-label">Preço Unitário</div>
        <div class="preco" style="color: var(--primary)">
          €{{ peca.precoUnitario }}
        </div>
      </div>
      <div style="text-align: right">
        <div class="meta-label">Valor em Stock</div>
        <div class="preco">
          €{{ (peca.precoUnitario * peca.stockDisponivel).toFixed(2) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  peca: {
    type: Object,
    required: true,
  },
})
defineEmits(['click'])

function stockPercent(p) {
  if (!p.stockMinimo) return p.stockDisponivel > 0 ? 100 : 0;
  return Math.min(100, Math.round((p.stockDisponivel / (p.stockMinimo * 2)) * 100));
}
function stockColor(p) {
  const pct = stockPercent(p);
  if (pct <= 20) return "#ef4444";
  if (pct <= 50) return "#f59e0b";
  return "#22c55e";
}
function estadoBadge(e) {
  const m = {
    OK: "badge-success",
    Baixo: "badge-warning",
    Crítico: "badge-danger",
  };
  return m[e] || "badge-gray";
}
</script>

<style scoped>
.peca-card {
  padding: 16px;
  cursor: pointer;
  transition: box-shadow var(--transition), transform var(--transition);
}
.peca-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.peca-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6px;
}
.peca-nome {
  font-weight: 700;
  font-size: 0.9rem;
}
.peca-codigo {
  font-family: "DM Mono", monospace;
  font-size: 0.72rem;
  color: var(--text-light);
  margin-top: 2px;
}
.peca-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 14px;
}

.peca-stock {
  margin-bottom: 14px;
}
.stock-nums {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 5px;
}
.stock-nums strong {
  color: var(--text);
}
.stock-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 99px;
  overflow: hidden;
  margin-bottom: 4px;
}
.stock-bar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.3s ease;
}
.stock-min-label {
  font-size: 0.7rem;
  color: var(--text-light);
}

.peca-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  margin-bottom: 14px;
}
.meta-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  margin-bottom: 2px;
}
.meta-value {
  font-weight: 500;
}

.peca-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}
.preco {
  font-weight: 700;
  font-size: 0.95rem;
}
</style>
