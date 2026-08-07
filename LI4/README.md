# TrotiFix — Gestão de Oficina

Sistema full-stack para gestão de uma oficina de reparação de trotinetes. Desenvolvido no âmbito da UC LI4 (Engenharia Informática, Universidade do Minho).

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | Vue 3 (Composition API), Vite, Vue Router 4, Chart.js, Lucide |
| Backend | Python 3, FastAPI, Uvicorn, Pydantic |
| Base de Dados | MySQL 8.0 (Docker) |
| Cache / Async | Redis 7 + Celery (Docker) |
| Auth | JWT (python-jose) + bcrypt |
| PDF | ReportLab |
| Testes | Pytest + pytest-cov |

## Pré-requisitos

- Docker + Docker Compose plugin
- Python 3.10+
- Node.js 20.x

## Instalação

```bash
bash scripts/install.sh
```

Este comando instala todas as dependências de sistema, cria o virtualenv Python, instala os pacotes Node, gera o ficheiro `.env`, e arranca os contentores Docker (MySQL + Redis).

## Como correr

```bash
bash scripts/shell/run-server.sh
```

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend (API) | http://localhost:8000 |

## Popular com dados de teste

```bash
bash scripts/shell/seed.sh
```

### Credenciais de teste

| Perfil | Username | Password |
|--------|----------|----------|
| Administrador | `admin` | `admin123` |
| Gestor | `gestor` | `gestor123` |
| Técnico | `tecnico` | `tecnico123` |
| Secretária | `secretaria` | `secretaria123` |

## Scripts disponíveis

| Script | Descrição |
|--------|-----------|
| `scripts/install.sh` | Instalação completa (dependências + Docker + seed) |
| `scripts/shell/run-server.sh` | Arranca MySQL, backend e frontend |
| `scripts/shell/seed.sh` | Popula a BD com dados de exemplo |
| `scripts/shell/clean-db.sh` | Limpa todos os dados da BD |
| `scripts/shell/setup.sh` | Setup rápido (sem instalar dependências de sistema) |

## Testes

```bash
cd backend && bash tests/run_coverage.sh
```

## Estrutura do projeto

```
app/
├── backend/              # API FastAPI
│   ├── main.py           # Ponto de entrada
│   ├── Model/            # Modelos de domínio (Clientes, OS, Stock, etc.)
│   ├── Routers/          # Endpoints da API
│   └── tests/            # Testes unitários, integração, sistema e aceitação
├── frontend/             # SPA Vue 3
│   └── src/
│       ├── views/        # Páginas
│       ├── components/   # Componentes reutilizáveis
│       ├── composables/  # Lógica reativa partilhada
│       ├── store/        # Estado global
│       └── config/       # Constantes por domínio
├── scripts/              # Scripts de instalação e execução
├── docker-compose.yml    # MySQL + Redis
└── seed-data.json        # Dados de seed
```

## Funcionalidades

- Gestão de clientes, trotinetes e peças
- Ordens de Serviço com ciclo de vida (Diagnóstico → Resposta → Reparação → Faturação → Encerramento)
- Faturação com geração de PDF
- Relatórios económicos, de stock e de performance (Celery + Redis)
- Autenticação JWT com controlo de permissões por perfil
- Dashboard com métricas e alertas de stock
