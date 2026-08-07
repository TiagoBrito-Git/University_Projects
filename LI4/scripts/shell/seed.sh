#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if ! docker ps >/dev/null 2>&1; then
    exec sg docker -c "'$0' $*"
fi

if [ -f "$ROOT/.env" ]; then
    set -a
    source "$ROOT/.env"
    set +a
fi

export DB_HOST="${DB_HOST:-127.0.0.1}"
export DB_PORT="${DB_PORT:-3307}"
export DB_USER="${DB_USER:-api_user}"
export DB_PASSWORD="${DB_PASSWORD:-api123}"
export DB_NAME="${DB_NAME:-scooterfix}"

echo "A semear dados de exemplo..."
echo ""

# mysql
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^scooterfix_db$'; then
    echo "[1/2] MySQL: ok."
else
    echo "[1/2] A ligar MySQL..."
    cd "$ROOT" && docker compose up -d
    for i in $(seq 1 30); do
        if docker exec scooterfix_db mysqladmin ping -h localhost -u api_user -papi123 --silent 2>/dev/null; then
            echo "  MySQL pronto."
            break
        fi
        sleep 2
    done
fi

# seed (nao precisa do backend a correr)
source "$ROOT/venv/bin/activate"

echo "[2/2] A inserir dados..."
cd "$ROOT/backend"
python seed_data.py

echo ""
echo "Seed concluido!"
echo ""
echo "Dados inseridos:"
echo "  - 4 users (admin, gestor, tecnico, secretaria)"
echo "  - 5 clientes"
echo "  - 5 trotinetes"
echo "  - 6 pecas"
echo "  - 1 ordem de servico"
echo "  - 2 faturas"
echo ""
echo "Logins:"
echo "  admin / admin123"
echo "  gestor / gestor123"
echo "  tecnico / tecnico123"
echo "  secretaria / secretaria123"
echo ""


