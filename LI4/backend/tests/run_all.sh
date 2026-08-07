#!/usr/bin/env bash
# Executa toda a suíte: unitários → integração → sistema → aceitação.
# Arranca Docker Compose automaticamente se o MySQL não estiver disponível.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT"

[[ -d "../venv" ]] || { echo "[erro] Virtualenv não encontrado em ../venv." >&2; exit 1; }
source ../venv/bin/activate

source tests/_wait_db.sh

PASS=0
FAIL=0

run() {
  local label="$1"; shift
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $label"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if python -m pytest "$@" -v; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
  fi
}

run "Testes Unitários" \
  tests/ \
  --ignore=tests/test_integration.py \
  --ignore=tests/test_sistema.py \
  --ignore=tests/test_aceitacao.py

if _wait_db; then
  run "Testes de Integração"  tests/test_integration.py -m integration
  run "Testes de Sistema"     tests/test_sistema.py     -m sistema
  run "Testes de Aceitação"   tests/test_aceitacao.py   -m aceitacao
fi

_stop_docker_if_started

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Resultado: ${PASS} conjuntos OK  |  ${FAIL} conjuntos com falhas"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ $FAIL -eq 0 ]]
