<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal" style="max-width: 620px">
      <div class="modal-header">
        <div>
          <h2>Registar Intervenção</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px">
            OS #{{ ordem?.id }}
          </p>
        </div>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">

        <div class="form-group">
          <label>Descrição da Intervenção <span class="required">*</span></label>
          <textarea
            v-model="formIntervencao.descricao"
            class="form-control"
            rows="3"
            placeholder="Descreva o trabalho realizado nesta intervenção..."
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Tempo de Mão-de-obra <span class="required">*</span></label>
            <input
              v-model="formIntervencao.tempo"
              class="form-control"
              type="time"
            />
          </div>
          <div class="form-group">
            <label>Custo Mão-de-obra</label>
            <div class="custo-preview">
              <span class="custo-label">{{ custoMaoObraIntervencao.toFixed(2) }} €</span>
              <span class="custo-sub">@ {{ taxaMaoObra }}€/hora</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>Peças Utilizadas</label>
          <div class="pecas-list">
            <div
              v-for="peca in pecasDisponiveis"
              :key="peca.id"
              class="peca-item"
              :class="{
                selected: formIntervencao.pecas[peca.id]?.quantidade > 0,
                'sem-stock': peca.stockDisponivel <= 0
              }"
              @click="peca.stockDisponivel > 0 && togglePecaIntervencao(peca.id)"
            >
              <div class="peca-check">
                <span v-if="formIntervencao.pecas[peca.id]?.quantidade > 0">✓</span>
              </div>
              <div class="peca-info">
                <div class="peca-nome">{{ peca.nome }}</div>
                <div class="peca-ref">
                  Stock: {{ peca.stockDisponivel }}
                  <span v-if="peca.stockDisponivel <= 0" class="stock-zero"> — Sem stock</span>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 8px">
                <input
                  v-if="formIntervencao.pecas[peca.id]?.quantidade > 0"
                  v-model.number="formIntervencao.pecas[peca.id].quantidade"
                  type="number"
                  min="1"
                  :max="peca.stockDisponivel"
                  class="qty-input"
                  @click.stop
                />
                <div class="peca-preco">{{ peca.precoUnitario?.toFixed(2) }} €</div>
              </div>
            </div>
            <div v-if="!pecasDisponiveis?.length" class="peca-empty">Nenhuma peça disponível.</div>
          </div>
        </div>

        <div class="custo-resumo" v-if="custoIntervencaoTotal > 0">
          <div class="custo-linha">
            <span>Peças</span>
            <span>{{ custoPecasIntervencao.toFixed(2) }} €</span>
          </div>
          <div class="custo-linha">
            <span>Mão-de-obra</span>
            <span>{{ custoMaoObraIntervencao.toFixed(2) }} €</span>
          </div>
          <div class="custo-linha total">
            <span>Total desta Intervenção</span>
            <span>{{ custoIntervencaoTotal.toFixed(2) }} €</span>
          </div>
        </div>

        <div v-if="intervencaoErro" class="alert-erro"><TriangleAlert :size="18" /> {{ intervencaoErro }}</div>
        <div v-if="intervencaoSucesso" class="alert-sucesso"><CheckCircle :size="18" /> {{ intervencaoSucesso }}</div>

        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px">
          <button class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button class="btn btn-primary" @click="submeterIntervencao">
            <Wrench :size="18" /> Guardar Intervenção
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>

import { CheckCircle } from "@lucide/vue"
import { TriangleAlert } from "@lucide/vue"
import { Wrench } from "@lucide/vue"
import { ref, reactive, computed } from "vue";
import { useOS } from "@/composables/useOS";
import { useToast } from "@/composables/useToast";

const { registarIntervencao } = useOS();
const { toast } = useToast();

const props = defineProps({
  modalOpen: { type: Boolean, default: false },
  ordem: { type: Object, default: null },
  pecasDisponiveis: { type: Array, default: () => [] },
  taxaMaoObra: { type: Number, default: 20 },
});

const emit = defineEmits(["close"]);

const intervencaoErro = ref("");
const intervencaoSucesso = ref("");

const formIntervencao = reactive({
  descricao: "",
  tempo: "",
  pecas: {},
});

function togglePecaIntervencao(id) {
  if (formIntervencao.pecas[id]) {
    delete formIntervencao.pecas[id];
  } else {
    formIntervencao.pecas[id] = { quantidade: 1 };
  }
}

function timeToHoras(timeStr) {
  if (!timeStr) return 0;
  const [h, m] = timeStr.split(":").map(Number);
  return h + m / 60;
}

const custoPecasIntervencao = computed(() => {
  return Object.entries(formIntervencao.pecas).reduce((acc, [id, { quantidade }]) => {
    const peca = props.pecasDisponiveis?.find((p) => p.id === Number(id));
    return acc + (peca?.precoUnitario ?? 0) * (Number(quantidade) || 0);
  }, 0);
});

const custoMaoObraIntervencao = computed(() => {
  return timeToHoras(formIntervencao.tempo) * props.taxaMaoObra;
});

const custoIntervencaoTotal = computed(
  () => custoPecasIntervencao.value + custoMaoObraIntervencao.value
);

function validarIntervencao() {
  if (!formIntervencao.descricao.trim()) return "A descrição é obrigatória.";
  if (!formIntervencao.tempo || timeToHoras(formIntervencao.tempo) <= 0) return "O tempo de mão-de-obra deve ser maior que 0.";
  for (const [id, { quantidade }] of Object.entries(formIntervencao.pecas)) {
    const qty = Number(quantidade);
    if (qty <= 0) return "A quantidade de cada peça deve ser maior que 0.";
    const peca = props.pecasDisponiveis?.find((p) => p.id === Number(id));
    if (!peca) continue;
    if (qty > peca.stockDisponivel)
      return `Stock insuficiente para "${peca.nome}" (disponível: ${peca.stockDisponivel}).`;
  }
  return null;
}

async function submeterIntervencao() {
  intervencaoErro.value = "";
  const erro = validarIntervencao();
  if (erro) { intervencaoErro.value = erro; return; }

  const tempoEmHoras = timeToHoras(formIntervencao.tempo);

  try {
    await registarIntervencao(props.ordem.id, {
      descricao: formIntervencao.descricao,
      tempo: tempoEmHoras,
      pecas: formIntervencao.pecas,
    });
    emit("close");
    toast("Intervenção registada com sucesso!", "success");
  } catch (err) {
    toast(err.message);
  }
}
</script>

<style scoped>
.required {
  color: var(--danger);
}
.pecas-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 6px;
}
.peca-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background var(--transition);
  border: 1px solid transparent;
}
.peca-item:hover {
  background: var(--bg);
}
.peca-item.selected {
  background: var(--primary-light, #eff6ff);
  border-color: var(--primary);
}
.peca-item.sem-stock {
  opacity: 0.45;
  cursor: not-allowed;
}
.stock-zero {
  color: var(--danger);
  font-weight: 600;
}
.peca-check {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary);
  flex-shrink: 0;
  transition: border-color var(--transition);
}
.peca-item.selected .peca-check {
  border-color: var(--primary);
  background: var(--primary);
  color: white;
}
.peca-info {
  flex: 1;
}
.peca-nome {
  font-size: 0.875rem;
  font-weight: 600;
}
.peca-ref {
  font-size: 0.72rem;
  color: var(--text-muted);
}
.peca-preco {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--primary);
  min-width: 56px;
  text-align: right;
}
.qty-btn {
  width: 26px;
  height: 26px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--bg);
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.qty-btn:hover { background: var(--border); }
.qty-input {
  width: 60px;
  padding: 4px 6px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  text-align: center;
}
.qty-input:focus {
  outline: none;
  border-color: var(--primary);
}
.peca-empty {
  padding: 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.8rem;
}
.custo-preview {
  display: flex;
  align-items: baseline;
  gap: 6px;
  padding: 10px 12px;
  background: var(--bg);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  margin-top: 4px;
}
.custo-label {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary);
}
.custo-sub {
  font-size: 0.72rem;
  color: var(--text-muted);
}
.custo-resumo {
  margin-top: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}
.custo-linha {
  display: flex;
  justify-content: space-between;
  padding: 8px 14px;
  font-size: 0.85rem;
  border-bottom: 1px solid var(--border);
}
.custo-linha:last-child {
  border-bottom: none;
}
.custo-linha.total {
  font-weight: 700;
  background: var(--primary-light, #eff6ff);
  color: var(--primary);
  font-size: 0.95rem;
}
.alert-erro {
  margin-top: 12px;
  padding: 10px 14px;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-left: 3px solid var(--danger);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: #be123c;
}
.alert-sucesso {
  margin-top: 12px;
  padding: 10px 14px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-left: 3px solid var(--success);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: #15803d;
}
</style>
