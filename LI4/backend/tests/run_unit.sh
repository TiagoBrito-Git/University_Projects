#!/usr/bin/env bash
# Executa os testes unitários (sem dependências externas).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

cd "$ROOT"

if [[ ! -d "../venv" ]]; then
  echo "[erro] Virtualenv não encontrado em ../venv — crie-o primeiro." >&2
  exit 1
fi

source ../venv/bin/activate

echo "=== Testes Unitários ==="
python -m pytest tests/ \
  --ignore=tests/test_integration.py \
  --ignore=tests/test_sistema.py \
  --ignore=tests/test_aceitacao.py \
  -v "$@"
