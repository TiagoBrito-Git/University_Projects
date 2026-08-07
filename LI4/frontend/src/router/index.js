import { createRouter, createWebHashHistory } from 'vue-router'
import { STORAGE_KEY } from '@/config/shared/constants'

const routes = [
  { path: '/', redirect: '/login' },
  { 
    path: '/login', 
    component: () => import('@/views/LoginView.vue'), 
    meta: { guest: true } },
  {
    path: '/dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/clientes',
    component: () => import('@/views/ClientesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/equipamentos',
    component: () => import('@/views/EquipamentosView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ordens-servico',
    component: () => import('@/views/OrdensServicoView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stock',
    component: () => import('@/views/StockView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/faturacao',
    component: () => import('@/views/FaturacaoView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/relatorios',
    component: () => import('@/views/RelatoriosView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/utilizadores',
    component: () => import('@/views/UtilizadoresView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to) => {
  const isLoggedIn = !!localStorage.getItem(STORAGE_KEY)
  if (to.meta.requiresAuth && !isLoggedIn) return '/login'
  if (to.meta.guest && isLoggedIn) return '/dashboard'
})

export default router
