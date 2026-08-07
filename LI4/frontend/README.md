# TrotiFix — Sistema de Gestão de Oficina

Aplicação Vue 3 que replica o design de um sistema de gestão para oficinas de trotinetes.

## 🚀 Como executar

```bash
# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# Build para produção
npm run build
```

Acede a `http://localhost:5173` após `npm run dev`.

## 🔑 Credenciais de teste

| Perfil  | Email                        | Password   |
|---------|------------------------------|------------|
| Admin   | joao.silva@oficina.pt        | qualquer   |
| Técnico | maria.santos@oficina.pt      | qualquer   |

## 📁 Estrutura do projeto

```
src/
├── assets/
│   └── main.css           # Estilos globais + CSS variables
├── components/
│   └── AppLayout.vue      # Layout principal (sidebar + topbar)
├── composables/
│   └── useAuth.js         # Autenticação (login/logout)
├── router/
│   └── index.js           # Vue Router com guards de autenticação
├── store/
│   └── index.js           # Estado global reativo com dados mock
└── views/
    ├── LoginView.vue       # Página de login
    ├── DashboardView.vue   # Dashboard com gráficos (Chart.js)
    ├── ClientesView.vue    # Gestão de clientes (CRUD)
    ├── EquipamentosView.vue # Gestão de trotinetes (CRUD)
    ├── OrdensServicoView.vue # Ordens de serviço com modal detalhe
    ├── StockView.vue       # Inventário de peças (CRUD)
    ├── FaturacaoView.vue   # Faturas e pagamentos
    └── RelatoriosView.vue  # Relatórios e gráficos
```

## 🛠️ Tecnologias

- **Vue 3** — Composition API
- **Vue Router 4** — Navegação com hash history
- **Chart.js + vue-chartjs** — Gráficos (bar, line, pie, doughnut)
- **Vite** — Build tool
- **CSS Variables** — Theming consistente sem preprocessador

## 🎨 Design

- Paleta: azul primário `#1a56db`, fundo `#f8f9fb`, tipografia `DM Sans`
- Layout sidebar fixo 240px + conteúdo principal
- Responsivo: sidebar colapsa em mobile com overlay
- Componentes reutilizáveis: `.card`, `.badge`, `.btn`, `.stat-card`, `.modal`, `.form-control`

## ✨ Funcionalidades implementadas

- ✅ Login com sugestões de email e guard de rota
- ✅ Dashboard com 4 KPIs, gráfico de barras e gráfico circular
- ✅ CRUD completo de Clientes, Equipamentos, Peças
- ✅ Ordens de Serviço com filtros por tabs e modal de detalhe
- ✅ Stock com barra de progresso de inventário e filtro por categoria
- ✅ Faturação com tabela, modal de detalhe e simulação de PDF
- ✅ Relatórios com 4 gráficos distintos
- ✅ Responsividade mobile
- ✅ Transições e hover effects em todos os cards
