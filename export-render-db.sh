#!/usr/bin/env bash
# Export Render's production Postgres database to a local file, as a
# pg_dump custom-format (compressed, pg_restore-able) archive.
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

: "${RENDER_DATABASE_URL:?Set RENDER_DATABASE_URL in .env (see .env-example) to the Render External Database URL before running this script}"

if [ $# -ne 1 ]; then
  echo "Usage: $0 <output-file>" >&2
  exit 1
fi

OUTPUT="$1"
mkdir -p "$(dirname "$OUTPUT")"

echo "Exporting Render database to $OUTPUT..."
pg_dump "$RENDER_DATABASE_URL" -Fc -f "$OUTPUT"
echo "Done. Restore with: pg_restore -d <target-database> $OUTPUT"
