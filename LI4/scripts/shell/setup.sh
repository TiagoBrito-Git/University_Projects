#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INSTALL_DOCKER=false

for arg in "$@"; do
    case "$arg" in
        --install-docker) INSTALL_DOCKER=true ;;
        *) echo "Uso: $0 [--install-docker]" && exit 1 ;;
    esac
done

install_docker() {
    echo "  A instalar Docker..."
    if curl -fsSL https://get.docker.com | sudo sh; then
        sudo usermod -aG docker "$USER"
        echo "  Docker instalado. Faz logout e login outra vez para usar sem sudo."
    else
        echo "  Erro ao instalar Docker. Instala manualmente:"
        echo "    curl -fsSL https://get.docker.com | sudo sh"
        exit 1
    fi
}

echo "TrotiFix - Setup inicial"
echo ""

# verifica se docker existe
if command -v docker &>/dev/null; then
    echo "[1/5] Docker: ok"
else
    echo "[1/5] Docker nao encontrado."
    if [ "$INSTALL_DOCKER" = true ]; then
        install_docker
    else
        echo ""
        echo "  Usa --install-docker para instalar automaticamente, ou instala manualmente:"
        echo "    curl -fsSL https://get.docker.com | sudo sh"
        echo "    sudo usermod -aG docker \$USER"
        echo "    (faz logout e login outra vez)"
        echo ""
        exit 1
    fi
fi

# mysql
echo "[2/5] A ligar MySQL..."
cd "$ROOT" && docker compose down -v 2>/dev/null || true
docker compose up -d
echo "  A aguardar MySQL..."
for i in $(seq 1 30); do
    if docker exec scooterfix_db mysql -u root -proot -e "SELECT 1" > /dev/null 2>&1; then
        echo "  MySQL pronto."
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "  ERRO: MySQL nao ligou a tempo."
        exit 1
    fi
    sleep 2
done

# criar BD e tabelas (os scripts de init já correm automaticamente no arranque do container)
echo "[3/5] A criar base de dados e tabelas..."
SQL_SCRIPT="$ROOT/scripts/sql/creation_script.sql"
if [ -f "$SQL_SCRIPT" ]; then
    docker exec -i scooterfix_db mysql -u root -proot < "$SQL_SCRIPT" 2>/dev/null && \
        echo "  Base de dados criada." || \
        echo "  (ja foi criada pelo container ao arrancar)"
else
    echo "  AVISO: $SQL_SCRIPT nao encontrado — base de dados nao criada."
fi

# python venv
echo "[4/5] A preparar Python..."
if [ -d "$ROOT/venv" ]; then
    echo "  venv ja existe."
else
    python3 -m venv "$ROOT/venv"
    echo "  venv criado."
fi

source "$ROOT/venv/bin/activate"
pip install -r "$ROOT/backend/requirements.txt" --quiet
echo "  dependencias Python instaladas."

# frontend
echo "[5/5] A preparar frontend..."
if [ -d "$ROOT/frontend/node_modules" ]; then
    echo "  node_modules ja existe."
else
    cd "$ROOT/frontend"
    npm install --silent
    echo "  dependencias Node instaladas."
fi

# .env
echo "  A verificar .env..."
if [ ! -f "$ROOT/.env" ]; then
    echo ""
    echo "  Cria um ficheiro .env na raiz com:"
    echo "    DB_HOST=127.0.0.1"
    echo "    DB_USER=api_user"
    echo "    DB_PASSWORD=api123"
    echo "    DB_NAME=scooterfix"
    echo "    DB_PORT=3307"
    echo "    SECRET_KEY=scooterfix_secret_key"
    echo ""
fi

echo ""
echo "Setup completo!"
echo ""
echo "Proximos passos:"
echo "  scripts/shell/seed.sh         # popular BD com dados de exemplo"
echo "  scripts/shell/run-server.sh   # correr servidor"
echo "  scripts/shell/view-data.sh    # ver dados (noutro terminal)"
