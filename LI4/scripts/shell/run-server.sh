#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# se docker n da logo, tenta com sg docker (caso o user ainda n fez logout)
if ! docker ps >/dev/null 2>&1; then
    exec sg docker -c "'$0' $*"
fi

export DB_HOST="${DB_HOST:-127.0.0.1}"
export DB_PORT="${DB_PORT:-3307}"
export DB_USER="${DB_USER:-api_user}"
export DB_PASSWORD="${DB_PASSWORD:-api123}"
export DB_NAME="${DB_NAME:-scooterfix}"

echo "A iniciar servidores..."
echo ""

# mysql
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^scooterfix_db$'; then
    echo "[1/3] MySQL: ja esta a correr."
else
    echo "[1/3] A ligar MySQL (docker)..."
    cd "$ROOT" && docker compose up -d
    for i in $(seq 1 30); do
        if docker exec scooterfix_db mysql -u root -proot -e "SELECT 1" > /dev/null 2>&1; then
            echo "  MySQL pronto."
            break
        fi
        sleep 2
    done
fi

# backend
echo "[2/3] A ligar backend..."
if [[ -f "$ROOT/.env" ]]; then
    set -a && source "$ROOT/.env" && set +a
fi
source "$ROOT/venv/bin/activate"
cd "$ROOT/backend"
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

for i in $(seq 1 15); do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "  Backend pronto -> http://localhost:8000"
        break
    fi
    sleep 1
done

# frontend
cd "$ROOT/frontend"
echo "[3/3] A ligar frontend..."
npm run dev &
FRONTEND_PID=$!

# limpeza ao sair
cleanup() {
    echo ""
    echo "A desligar servidores..."
    kill "${BACKEND_PID:-}" "${FRONTEND_PID:-}" 2>/dev/null
    wait "${BACKEND_PID:-}" "${FRONTEND_PID:-}" 2>/dev/null
    echo "Servidores desligados."
}
trap cleanup INT TERM

echo ""
echo "Servidores a correr!"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo ""
echo "Ctrl+C para parar."
echo ""
wait
