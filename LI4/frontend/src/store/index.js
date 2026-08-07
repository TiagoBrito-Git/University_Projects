import { reactive, computed } from "vue";

const state = reactive({
  clientes: [],
  ordensServico: [],
  pecas: [],
  faturas: [],
  utilizadores: [],
})

export function useStore() {
  return {
    clientes: computed(() => state.clientes),
    ordensServico: computed(() => state.ordensServico),
    pecas: computed(() => state.pecas),
    faturas: computed(() => state.faturas),
    utilizadores: computed(() => state.utilizadores),
  }
}

export function setStoreCollection(name, data) {
  state[name] = data
}

export function pushToStoreCollection(name, item) {
  state[name].push(item)
}

export function getStoreCollection(name) {
  return state[name]
}
