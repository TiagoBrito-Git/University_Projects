<template>
  <div class="modal-overlay" v-if="modalOpen" @click.self="$emit('close')">
    <div class="modal" style="max-width: 460px">
      <div class="modal-header">
        <div>
          <h2>Resposta do Cliente</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px">
            OS #{{ ordem?.id }}
          </p>
        </div>
        <button class="modal-close" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-body">

        <div class="resposta-valor-bloco" v-if="ordem?.valorEstimado">
          <div class="detail-label">Orçamento Apresentado</div>
          <div class="valor-num">€{{ ordem.valorEstimado.toFixed(2) }}</div>
        </div>

        <div class="form-group" style="margin-top: 16px">
          <label>Decisão do Cliente <span class="required">*</span></label>
          <div class="resposta-opcoes">
            <div
              class="resposta-opcao"
              :class="{ selected: formResposta.aceitou === true }"
              @click="formResposta.aceitou = true"
            >
              <span class="resposta-icone"><CheckCircle :size="18" /></span>
              <div>
                <div class="resposta-titulo">Aceite</div>
                <div class="resposta-sub">Avança para "Em Reparação"</div>
              </div>
            </div>
            <div
              class="resposta-opcao recusa"
              :class="{ selected: formResposta.aceitou === false }"
              @click="formResposta.aceitou = false"
            >
              <span class="resposta-icone"><XCircle :size="18" /></span>
              <div>
                <div class="resposta-titulo">Recusado</div>
                <div class="resposta-sub">Ordem passa a "Cancelada"</div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>Observações <span style="color: var(--text-muted); font-weight: 400">(opcional)</span></label>
          <textarea
            v-model="formResposta.observacoes"
            class="form-control"
            rows="3"
            placeholder="Ex: Cliente pediu para aguardar, solicitou desconto, etc."
          ></textarea>
        </div>

        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px">
          <button class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
          <button
            class="btn btn-primary"
            :disabled="formResposta.aceitou === null"
            @click="submeterResposta"
          >
            <CheckCircle :size="18" /> Confirmar Resposta
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>

import { CheckCircle } from "@lucide/vue"
import { XCircle } from "@lucide/vue"
import { reactive } from "vue";
import { useOS } from "@/composables/useOS";
import { useToast } from "@/composables/useToast";

const { registarDecisaoCliente } = useOS();
const { toast } = useToast();

const props = defineProps({
  modalOpen: { type: Boolean, default: false },
  ordem: { type: Object, default: null },
});

const emit = defineEmits(["close"]);

const formResposta = reactive({
  aceitou: null,
  observacoes: "",
});

async function submeterResposta() {
  if (formResposta.aceitou === null) return;
  const decisao = formResposta.aceitou ? "Aprovado" : "Rejeitado";
  try {
    await registarDecisaoCliente(props.ordem.id, decisao);
    emit("close");
    toast("Resposta registada com sucesso!", "success");
  } catch (err) {
    toast(err.message);
  }
}
</script>

<style scoped>
.resposta-valor-bloco {
  background: var(--bg);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  border-left: 3px solid var(--primary);
}
.valor-num {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary);
}
.resposta-opcoes {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 6px;
}
.resposta-opcao {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: 2px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: border-color var(--transition), background var(--transition);
}
.resposta-opcao:hover {
  border-color: var(--primary);
  background: var(--primary-light, #eff6ff);
}
.resposta-opcao.selected {
  border-color: var(--primary);
  background: var(--primary-light, #eff6ff);
}
.resposta-opcao.recusa:hover,
.resposta-opcao.recusa.selected {
  border-color: var(--danger);
  background: #fff1f2;
}
.resposta-icone {
  font-size: 1.3rem;
  flex-shrink: 0;
}
.resposta-titulo {
  font-weight: 700;
  font-size: 0.9rem;
}
.resposta-sub {
  font-size: 0.75rem;
  color: var(--text-muted);
}
</style>
