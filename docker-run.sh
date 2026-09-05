#!/usr/bin/env bash
# Build the zink Docker image and run it locally against its own throwaway
# Postgres container, mirroring the container's real start mechanism
# (collectstatic, migrate, loaddata blog, then uvicorn).
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

: "${SECRET_KEY:?Set SECRET_KEY in .env (see .env-example) before running this script}"
: "${POSTGRES_USER:=zink}"
: "${POSTGRES_PASSWORD:=zink}"
: "${POSTGRES_DB:=zink}"
: "${DEBUG:=False}"
PORT="${PORT:-8080}"

NETWORK=zink-run-net
DB_CONTAINER=zink-run-db
APP_CONTAINER=zink-run-app
IMAGE=zink

docker network inspect "$NETWORK" >/dev/null 2>&1 || docker network create "$NETWORK" >/dev/null

if ! docker ps --format '{{.Names}}' | grep -qx "$DB_CONTAINER"; then
  docker rm -f "$DB_CONTAINER" >/dev/null 2>&1 || true
  docker run --name "$DB_CONTAINER" --network "$NETWORK" \
    -e POSTGRES_USER="$POSTGRES_USER" \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB="$POSTGRES_DB" \
    -d postgres:16 >/dev/null
  echo "Started $DB_CONTAINER, waiting for it to accept connections..."
  until docker exec "$DB_CONTAINER" pg_isready -U "$POSTGRES_USER" >/dev/null 2>&1; do
    sleep 1
  done
fi

docker build -t "$IMAGE" .

docker rm -f "$APP_CONTAINER" >/dev/null 2>&1 || true

docker run --name "$APP_CONTAINER" --network "$NETWORK" \
  -e SECRET_KEY="$SECRET_KEY" \
  -e DEBUG="$DEBUG" \
  -e RENDER=true \
  -e POSTGRES_HOST="$DB_CONTAINER" \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_USER="$POSTGRES_USER" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -e POSTGRES_DB="$POSTGRES_DB" \
  -p "$PORT":80 \
  -d "$IMAGE" >/dev/null

echo "zink is running at http://localhost:$PORT (docker logs -f $APP_CONTAINER)"
