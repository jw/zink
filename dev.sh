#!/usr/bin/env bash
# Run the Django dev server and the Canvas SCSS watcher together, so CSS
# edits show up without needing a separate terminal/manual rebuild.
set -euo pipefail
cd "$(dirname "$0")"

PIDS=()
cleanup() {
  kill "${PIDS[@]}" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

yarn watch:canvas-css &
PIDS+=("$!")

uv run manage.py runserver "$@" &
PIDS+=("$!")

wait -n "${PIDS[@]}"
