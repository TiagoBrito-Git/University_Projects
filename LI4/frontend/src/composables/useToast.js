import { ref } from 'vue'

const toasts = ref([])
let nextId = 0

export function useToast() {
  function toast(message, type = 'error', duration = 4000) {
    const id = nextId++
    toasts.value = [...toasts.value, { id, message, type }]
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, duration)
  }

  function dismiss(id) {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return { toasts, toast, dismiss }
}
