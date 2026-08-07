<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="t in toasts"
          :key="t.id"
          class="toast"
          :class="t.type"
          @click="dismiss(t.id)"
        >
          {{ t.message }}
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from "@/composables/useToast"
const { toasts, dismiss } = useToast()
</script>

<style>
.toast-container {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}
.toast {
  pointer-events: auto;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,.15);
  cursor: pointer;
  max-width: 400px;
  line-height: 1.4;
}
.toast.error { background: #ef4444; }
.toast.success { background: #16a34a; }
.toast.warning { background: #f59e0b; }
.toast.info { background: #3b82f6; }

.toast-enter-active { transition: all .25s ease; }
.toast-leave-active { transition: all .2s ease; }
.toast-enter-from { opacity: 0; transform: translateX(40px); }
.toast-leave-to { opacity: 0; transform: translateX(40px); }
</style>
