<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-logo"><Wrench :size="32" /></div>
      <h1 class="login-title">TrotiFix</h1>
      <p class="login-sub">Sistema de Gestão de Oficina</p>
      <slot />
    </div>
    <footer class="login-footer">Projeto Académico · Engenharia Informática</footer>
  </div>
</template>

<style scoped>
.login-page { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f0f4ff; padding: 24px; }
.login-card { background: white; border-radius: 16px; box-shadow: 0 4px 32px rgba(0,0,0,0.1); padding: 40px 36px; width: 100%; max-width: 400px; text-align: center; }
.login-logo { font-size: 2.8rem; background: var(--primary); width: 72px; height: 72px; border-radius: 18px; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; }
.login-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }
.login-sub { color: var(--text-muted); font-size: 0.875rem; margin-bottom: 28px; }
.login-footer { margin-top: 24px; font-size: 0.75rem; color: var(--text-light); }
</style>
