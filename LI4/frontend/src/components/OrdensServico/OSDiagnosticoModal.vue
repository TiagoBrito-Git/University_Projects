<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal" style="max-width: 580px">
      <div class="modal-header">
        <div>
          <h2>Registar Diagnóstico</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px">
            OS #{{ ordem?.id }}
          </p>
        </div>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">

        <div class="form-group">
          <label>Descrição do Diagnóstico <span class="required">*</span></label>
          <textarea
            v-model="formDiag.descricao"
            class="form-control"
            rows="4"
            placeholder="Descreva o problema identificado, causa raiz, e trabalho necessário..."
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Tempo Estimado de Reparação <span class="required">*</span></label>
            <input
              v-model="formDiag.tempoEstimado"
              class="form-control"
              type="time"
            />
          </div>
          <div class="form-group">
            <label>Custo Mão-de-obra</label>
            <div class="custo-preview">
              <span class="custo-label">{{ custoMaoObra.toFixed(2) }} €</span>
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
              :class="{ selected: !!formDiag.pecas[peca.id] }"
            >
              <div class="peca-check" @click="togglePeca(peca.id)" style="cursor:pointer">
                <span v-if="formDiag.pecas[peca.id]">✓</span>
              </div>
              <div class="peca-info" @click="togglePeca(peca.id)" style="cursor:pointer; flex:1">
                <div class="peca-nome">{{ peca.nome }}</div>
                <div class="peca-ref" v-if="peca.referencia">Ref: {{ peca.referencia }}</div>
              </div>
              <div v-if="formDiag.pecas[peca.id]" style="display:flex; align-items:center; gap:6px">
                <button class="qty-btn" @click.stop="setPecaQty(peca.id, formDiag.pecas[peca.id] - 1)">−</button>
                <input
                  class="qty-input"
                  type="number"
                  min="1"
                  :value="formDiag.pecas[peca.id]"
                  @click.stop
                  @change.stop="setPecaQty(peca.id, $event.target.value)"
                />
                <button class="qty-btn" @click.stop="setPecaQty(peca.id, formDiag.pecas[peca.id] + 1)">+</button>
              </div>
              <div class="peca-preco">{{ ((peca.precoUnitario ?? 0) * (formDiag.pecas[peca.id] || 1)).toFixed(2) }} €</div>
            </div>
            <div v-if="!pecasDisponiveis?.length" class="peca-empty">
              Nenhuma peça disponível no stock.
            </div>
          </div>
        </div>

        <div class="custo-resumo" v-if="formDiag.tempoEstimado || Object.keys(formDiag.pecas).length > 0">
          <div class="custo-linha">
            <span>Peças ({{ Object.keys(formDiag.pecas).length }})</span>
            <span>{{ custoPecas.toFixed(2) }} €</span>
          </div>
          <div class="custo-linha">
            <span>Mão-de-obra</span>
            <span>{{ custoMaoObra.toFixed(2) }} €</span>
          </div>
          <div class="custo-linha total">
            <span>Total Estimado</span>
            <span>{{ custoTotal.toFixed(2) }} €</span>
          </div>
        </div>

        <div class="alert-erro" v-if="formError">{{ formError }}</div>
        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px">
          <button class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button
            class="btn btn-primary"
            :disabled="!formDiag.descricao.trim() || !formDiag.tempoEstimado"
            @click="submeterDiagnostico"
          >
            <CheckCircle :size="18" /> Guardar Diagnóstico
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>

import { CheckCircle } from "@lucide/vue"
import { ref, reactive, computed } from "vue";
import { useOS } from "@/composables/useOS";
import { useToast } from "@/composables/useToast";

const { registarDiagnostico } = useOS();
const { toast } = useToast();

const props = defineProps({
  modalOpen: { type: Boolean, default: false },
  ordem: { type: Object, default: null },
  pecasDisponiveis: { type: Array, default: () => [] },
  taxaMaoObra: { type: Number, default: 20 },
});

const emit = defineEmits(["close"]);

const formError = ref("")
const formDiag = reactive({
  descricao: "",
  tempoEstimado: "",
  pecas: {},
});

function togglePeca(id) {
  if (formDiag.pecas[id]) {
    delete formDiag.pecas[id];
  } else {
    formDiag.pecas[id] = 1;
  }
}

function setPecaQty(id, qty) {
  const n = parseInt(qty);
  if (n <= 0 || isNaN(n)) {
    delete formDiag.pecas[id];
  } else {
    formDiag.pecas[id] = n;
  }
}

function timeToHoras(timeStr) {
  if (!timeStr) return 0;
  const [h, m] = timeStr.split(":").map(Number);
  return h + m / 60;
}

const custoPecas = computed(() => {
  return Object.entries(formDiag.pecas).reduce((acc, [id, qty]) => {
    const peca = props.pecasDisponiveis?.find((p) => p.id === Number(id));
    return acc + (peca?.precoUnitario ?? 0) * qty;
  }, 0);
});

const custoMaoObra = computed(() => {
  return timeToHoras(formDiag.tempoEstimado) * props.taxaMaoObra;
});

const custoTotal = computed(() => custoPecas.value + custoMaoObra.value);

async function submeterDiagnostico() {
  formError.value = ""
  if (!formDiag.descricao.trim()) {
    formError.value = "A descrição do diagnóstico é obrigatória."
    return
  }
  if (!formDiag.tempoEstimado) {
    formError.value = "O tempo estimado de reparação é obrigatório."
    return
  }
  const tempoEmHoras = timeToHoras(formDiag.tempoEstimado);
  try {
    await registarDiagnostico(props.ordem.id, {
      descricao: formDiag.descricao,
      tempo_estimado: tempoEmHoras,
      pecas: { ...formDiag.pecas },
    });
    emit("close");
    toast("Diagnóstico registado com sucesso!", "success");
  } catch (err) {
    formError.value = err.message
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
  width: 42px;
  text-align: center;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 2px 4px;
  font-size: 0.85rem;
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
  margin-top: 10px;
  padding: 10px 14px;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-left: 3px solid var(--danger);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: #be123c;
}
</style>
