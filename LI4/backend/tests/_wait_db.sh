#!/usr/bin/env bash
# Sourced por outros scripts.
# Arranca sempre o MySQL via Docker Compose e aguarda estar pronto.

_COMPOSE_FILE="$(dirname "$ROOT")/docker-compose.yml"
_DOCKER_STARTED=false

_db_acessivel() {
  python -c "
import mysql.connector, sys
try:
    mysql.connector.connect(host='localhost', port=3307,
        database='scooterfix', user='api_user', password='api123').close()
except Exception:
    sys.exit(1)
" 2>/dev/null
}

_wait_db() {
  if ! command -v docker &>/dev/null; then
    echo "[erro] Docker não encontrado. Instale Docker Desktop para correr os testes." >&2
    return 1
  fi

  if ! [[ -f "$_COMPOSE_FILE" ]]; then
    echo "[erro] docker-compose.yml não encontrado em $(dirname "$_COMPOSE_FILE")." >&2
    return 1
  fi

  echo "[docker] A arrancar MySQL com docker compose..."
  docker compose -f "$_COMPOSE_FILE" up -d db
  _DOCKER_STARTED=true

  local retries=30
  echo "[docker] A aguardar MySQL ficar pronto..."
  while ! _db_acessivel; do
    retries=$((retries - 1))
    if [[ $retries -le 0 ]]; then
      echo "[erro] MySQL não ficou disponível após 60s." >&2
      return 1
    fi
    sleep 2
  done
  echo "[docker] MySQL pronto."
}

_stop_docker_if_started() {
  if [[ "$_DOCKER_STARTED" == true ]]; then
    echo "[docker] A parar contentor MySQL..."
    docker compose -f "$_COMPOSE_FILE" stop db
  fi
}
