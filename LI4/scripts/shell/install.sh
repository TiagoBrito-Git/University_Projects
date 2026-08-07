#!/usr/bin/env bash
# Instala todas as dependências do projeto TrotiFix.
# Suporta Ubuntu/Debian e macOS.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# ─── cores ───────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[ok]${NC}  $*"; }
info() { echo -e "${YELLOW}[..]${NC}  $*"; }
err()  { echo -e "${RED}[erro]${NC} $*" >&2; }

# ─── sistema operativo ───────────────────────────────────
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    err "Sistema operativo não suportado: $OSTYPE"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   TrotiFix — Instalação completa     ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ─────────────────────────────────────────────────────────
# 1. DEPENDÊNCIAS DE SISTEMA
# ─────────────────────────────────────────────────────────
echo "── 1/5  Dependências de sistema ─────────────────────"

install_linux() {
    info "A atualizar lista de pacotes..."
    sudo apt-get update -qq 2>/dev/null || true

    # Python 3
    if command -v python3 &>/dev/null; then
        ok "Python3 já instalado: $(python3 --version)"
    else
        info "A instalar Python3..."
        sudo apt-get install -y python3 python3-pip python3-venv
        ok "Python3 instalado."
    fi

    # pip / venv
    if ! python3 -m pip --version &>/dev/null; then
        sudo apt-get install -y python3-pip
    fi
    if ! python3 -m venv --help &>/dev/null 2>&1; then
        sudo apt-get install -y python3-venv
    fi
    ok "pip + venv disponíveis."

    # Node.js / npm
    if command -v node &>/dev/null; then
        ok "Node.js já instalado: $(node --version)"
    else
        info "A instalar Node.js 20.x..."
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - 2>/dev/null
        sudo apt-get install -y nodejs
        ok "Node.js instalado: $(node --version)"
    fi

    # Docker
    if command -v docker &>/dev/null; then
        ok "Docker já instalado: $(docker --version)"
    else
        info "A instalar Docker..."
        curl -fsSL https://get.docker.com | sudo sh
        sudo usermod -aG docker "$USER"
        ok "Docker instalado. ATENÇÃO: faz logout/login para usar sem sudo."
    fi

    # Docker Compose plugin
    if docker compose version &>/dev/null 2>&1; then
        ok "Docker Compose disponível."
    else
        info "A instalar Docker Compose plugin..."
        sudo apt-get install -y docker-compose-plugin
        ok "Docker Compose instalado."
    fi
}

install_macos() {
    # Homebrew
    if ! command -v brew &>/dev/null; then
        info "A instalar Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ok "Homebrew instalado."
    else
        ok "Homebrew já instalado."
    fi

    # Python 3
    if command -v python3 &>/dev/null; then
        ok "Python3 já instalado: $(python3 --version)"
    else
        info "A instalar Python3..."
        brew install python3
        ok "Python3 instalado."
    fi

    # Node.js
    if command -v node &>/dev/null; then
        ok "Node.js já instalado: $(node --version)"
    else
        info "A instalar Node.js..."
        brew install node
        ok "Node.js instalado: $(node --version)"
    fi

    # Docker Desktop
    if command -v docker &>/dev/null; then
        ok "Docker já instalado: $(docker --version)"
    else
        err "Docker Desktop não encontrado. Instala em: https://www.docker.com/products/docker-desktop/"
        exit 1
    fi
}

if [[ "$OS" == "linux" ]]; then
    install_linux
else
    install_macos
fi

# ─────────────────────────────────────────────────────────
# 2. PYTHON — VENV E DEPENDÊNCIAS
# ─────────────────────────────────────────────────────────
echo ""
echo "── 2/5  Python — venv e dependências ───────────────"

if [[ -d "$ROOT/venv" ]]; then
    info "A recriar virtualenv..."
    rm -rf "$ROOT/venv" 2>/dev/null || sudo rm -rf "$ROOT/venv"
fi
info "A criar virtualenv..."
python3 -m venv "$ROOT/venv"
ok "venv criado."

source "$ROOT/venv/bin/activate"

info "A instalar dependências Python..."
pip install --upgrade pip -q
pip install -r "$ROOT/backend/requirements.txt" -q
pip install pytest-cov -q
ok "Dependências Python instaladas (incluindo pytest-cov)."

# ─────────────────────────────────────────────────────────
# 3. FRONTEND — NODE MODULES
# ─────────────────────────────────────────────────────────
echo ""
echo "── 3/5  Frontend — node_modules ────────────────────"

if [[ -d "$ROOT/frontend/node_modules" ]]; then
    info "A reinstalar dependências Node..."
    rm -rf "$ROOT/frontend/node_modules"
fi
info "A instalar dependências Node..."
cd "$ROOT/frontend"
npm install --silent
cd "$ROOT"
ok "Dependências Node instaladas."

# ─────────────────────────────────────────────────────────
# 4. FICHEIRO .env
# ─────────────────────────────────────────────────────────
echo ""
echo "── 4/5  Ficheiro .env ───────────────────────────────"

if [[ -f "$ROOT/.env" ]]; then
    ok ".env já existe."
else
    info "A criar .env com valores por defeito..."
    cat > "$ROOT/.env" <<'EOF'
DB_HOST=127.0.0.1
DB_PORT=3307
DB_USER=api_user
DB_PASSWORD=api123
DB_NAME=scooterfix
SECRET_KEY=scooterfix_secret_key
EOF
    ok ".env criado em $ROOT/.env"
fi

# ─────────────────────────────────────────────────────────
# 5. BASE DE DADOS — DOCKER
# ─────────────────────────────────────────────────────────
echo ""
echo "── 5/5  Base de dados — Docker ─────────────────────"

if docker info &>/dev/null 2>&1; then
    info "A remover contentores antigos (se existirem)..."
    docker rm -f scooterfix_db scooterfix_redis 2>/dev/null || true
    info "A iniciar MySQL e Redis via Docker Compose..."
    docker compose -f "$ROOT/docker-compose.yml" up -d

    info "A aguardar MySQL ficar pronto..."
    retries=30
    until docker compose -f "$ROOT/docker-compose.yml" exec -T db \
        mysqladmin ping -u api_user -papi123 --silent 2>/dev/null; do
        retries=$((retries - 1))
        [[ $retries -le 0 ]] && { err "MySQL não ficou disponível após 60s."; exit 1; }
        sleep 2
    done
    ok "MySQL pronto."
    ok "Redis a correr."
else
    err "Docker não está a correr. Inicia o Docker e corre este script novamente."
    exit 1
fi

# ─────────────────────────────────────────────────────────
# RESUMO
# ─────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════╗"
echo "║         Instalação concluída!        ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "  Para arrancar o servidor:"
echo "    bash scripts/shell/run-server.sh"
echo ""
echo "  Para popular a BD com dados de teste:"
echo "    bash scripts/shell/seed.sh"
echo ""
echo "  Para correr os testes com cobertura:"
echo "    cd backend && bash tests/run_all.sh"
echo ""
