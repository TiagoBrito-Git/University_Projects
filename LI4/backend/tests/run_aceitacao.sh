#!/usr/bin/env bash
# Executa os testes de aceitação BDD.
# Arranca Docker Compose automaticamente se o MySQL não estiver disponível.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT"

[[ -d "../venv" ]] || { echo "[erro] Virtualenv não encontrado em ../venv." >&2; exit 1; }
source ../venv/bin/activate

source tests/_wait_db.sh
_wait_db || exit 1

echo "=== Testes de Aceitação (BDD) ==="
python -m pytest tests/test_aceitacao.py -m aceitacao -v "$@"
EXIT_CODE=$?

_stop_docker_if_started
exit $EXIT_CODE
