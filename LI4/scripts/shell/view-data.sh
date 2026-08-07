#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "A consultar dados da API..."
echo ""

# ver se o backend ta a correr
if ! curl -s --max-time 3 http://localhost:8000/health > /dev/null 2>&1; then
    echo "ERRO: backend nao esta a correr."
    echo ""
    echo "Para ligar o backend: scripts/shell/run-server.sh"
    echo ""
    exit 1
fi

source "$ROOT/venv/bin/activate"

echo "A fazer login como admin..."
RESPONSE=$(curl -s --max-time 5 localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

TOKEN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null) || {
    echo "ERRO: nao foi possivel fazer login"
    echo ""
    echo "Provavelmente a base de dados esta vazia (sem utilizadores)"
    echo "Para popular a BD: scripts/shell/seed.sh"
    echo ""
    exit 1
}

echo "Token obtido."
echo ""

# buscar dados de cada endpoint
fetch() {
    local label="$1" url="$2"
    echo "--- $label ---"
    curl -s --max-time 5 "$url" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null || echo "(vazio ou erro)"
    echo ""
}

fetch "TROTINETES"     "http://localhost:8000/trotinetes/"
fetch "CLIENTES"       "http://localhost:8000/clientes/"
fetch "STOCK"          "http://localhost:8000/stock/"
fetch "ORDENS SERVICO" "http://localhost:8000/os/"
fetch "FATURAS"        "http://localhost:8000/fatura/"
fetch "UTILIZADORES"   "http://localhost:8000/utilizadores"

echo "Concluido!"
