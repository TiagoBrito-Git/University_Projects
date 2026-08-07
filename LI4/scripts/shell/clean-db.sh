#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if ! docker ps >/dev/null 2>&1; then
    exec sg docker -c "'$0' $*"
fi

export DB_HOST="${DB_HOST:-127.0.0.1}"
export DB_PORT="${DB_PORT:-3307}"
export DB_USER="${DB_USER:-api_user}"
export DB_PASSWORD="${DB_PASSWORD:-api123}"
export DB_NAME="${DB_NAME:-scooterfix}"

echo "A limpar a base de dados..."
echo ""
echo "ISTO VAI APAGAR TUDO DA BD!"
echo "Precisas mesmo de fazer isto? (ENTER para confirmar, Ctrl+C para cancelar)"
read -r

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

echo "[2/2] A apagar dados..."
source "$ROOT/venv/bin/activate"
cd "$ROOT/backend"
python seed_data.py --truncate-only

echo ""
echo "BD limpa!"
echo ""
echo "Para meter dados outra vez: scripts/shell/seed.sh"
