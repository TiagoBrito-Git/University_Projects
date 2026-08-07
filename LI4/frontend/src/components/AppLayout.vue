<template>
  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-brand">
        <div class="brand-icon"><Wrench :size="22" /></div>
        <div>
          <div class="brand-name">TrotiFix</div>
          <div class="brand-sub">Gestão de Oficina</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          @click="sidebarOpen = false"
        >
          <span class="nav-icon"><component :is="item.icon" :size="18" /></span>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ initials }}</div>
          <div>
            <div class="user-name">{{ currentUser?.name }}</div>
            <div class="user-role">{{ currentUser?.perfil }}</div>
          </div>
        </div>
        <button class="logout-btn" @click="logout" title="Sair"><LogOut :size="18" /></button>
      </div>
    </aside>

    <!-- Overlay mobile -->
    <div class="sidebar-overlay" v-if="sidebarOpen" @click="sidebarOpen = false" />

    <!-- Main -->
    <div class="main-wrap">
      <header class="topbar">
        <button class="menu-btn" @click="sidebarOpen = !sidebarOpen"><Menu :size="20" /></button>
        <div class="topbar-title">{{ pageTitle }}</div>
      </header>

      <main class="main-content">
        <slot />
      </main>
    </div>
  </div>
  <ToastContainer />
</template>

<script setup>

import { Wrench, LayoutDashboard, Users, Truck, ClipboardList, Package, DollarSign, BarChart3, UserCircle, LogOut, Menu } from "@lucide/vue"
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import ToastContainer from '@/components/ToastContainer.vue'

const { currentUser, logout } = useAuth()
const route = useRoute()
const sidebarOpen = ref(false)

const navItems = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/clientes', icon: Users, label: 'Clientes' },
  { path: '/equipamentos', icon: Truck, label: 'Equipamentos' },
  { path: '/ordens-servico', icon: ClipboardList, label: 'Ordens de Serviço' },
  { path: '/stock', icon: Package, label: 'Stock & Peças' },
  { path: '/faturacao', icon: DollarSign, label: 'Faturação' },
  { path: '/relatorios', icon: BarChart3, label: 'Relatórios' },
  { path: '/utilizadores', icon: UserCircle, label: 'Utilizadores' },
]

const pageTitles = {
  '/dashboard': 'Dashboard',
  '/clientes': 'Clientes',
  '/equipamentos': 'Equipamentos',
  '/ordens-servico': 'Ordens de Serviço',
  '/stock': 'Stock & Peças',
  '/faturacao': 'Faturação',
  '/relatorios': 'Relatórios',
  '/utilizadores': 'Utilizadores'
}

const pageTitle = computed(() => pageTitles[route.path] || '')
const initials = computed(() => {
  if (!currentUser.value) return '?'
  return currentUser.value.name.split(' ').map(n => n[0]).slice(0, 2).join('')
})
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; left: 0; bottom: 0;
  z-index: 200;
  transition: transform .25s ease;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px 16px;
  border-bottom: 1px solid var(--border);
}
.brand-icon { font-size: 1.4rem; }
.brand-name { font-weight: 700; font-size: .95rem; }
.brand-sub { font-size: .7rem; color: var(--text-muted); }

.sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: var(--radius-sm);
  font-size: .875rem;
  font-weight: 500;
  color: var(--text-muted);
  transition: background var(--transition), color var(--transition);
  margin-bottom: 2px;
}
.nav-item:hover { background: var(--bg); color: var(--text); }
.nav-item.router-link-active {
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
}
.nav-icon { font-size: 1rem; width: 20px; text-align: center; }

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
}
.user-info { flex: 1; display: flex; align-items: center; gap: 8px; min-width: 0; }
.user-avatar {
  width: 32px; height: 32px;
  background: var(--primary);
  color: #fff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .75rem; font-weight: 700;
  flex-shrink: 0;
}
.user-name { font-size: .8rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: .7rem; color: var(--text-muted); }
.logout-btn { color: var(--text-muted); font-size: 1rem; padding: 4px; border-radius: 4px; transition: color var(--transition); }
.logout-btn:hover { color: var(--danger); }

/* Main */
.main-wrap {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  height: var(--header-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 100;
}
.menu-btn { display: none; font-size: 1.2rem; color: var(--text-muted); padding: 4px 8px; border-radius: 4px; }
.topbar-title { font-weight: 700; font-size: 1rem; }

.main-content {
  flex: 1;
  padding: 28px 28px 40px;
  max-width: 1200px;
  width: 100%;
}

.sidebar-overlay { display: none; }

/* Mobile */
@media (max-width: 768px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); box-shadow: var(--shadow-md); }
  .main-wrap { margin-left: 0; }
  .menu-btn { display: flex; }
  .sidebar-overlay {
    display: block;
    position: fixed; inset: 0;
    background: rgba(0,0,0,.4);
    z-index: 199;
  }
  .main-content { padding: 20px 16px 32px; }
}
</style>
