#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${1:-http://127.0.0.1:8000}"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

write_file() {
  local file_path="$1"
  local content="$2"
  mkdir -p "$(dirname "$file_path")"
  printf "%s\n" "$content" > "$file_path"
  echo "[ok] wrote $file_path"
}

# Web client
if [ -d "$ROOT_DIR/hrrepozik" ]; then
  write_file "$ROOT_DIR/hrrepozik/.env.local" "API_BASE_URL=$API_BASE_URL"
fi

# Mobile client
if [ -d "$ROOT_DIR/hrrepozik-modile-2" ]; then
  write_file "$ROOT_DIR/hrrepozik-modile-2/.env.local" "API_BASE_URL=$API_BASE_URL"
fi

# Desktop client
if [ -d "$ROOT_DIR/repozik-desktop2" ]; then
  write_file "$ROOT_DIR/repozik-desktop2/.env.local" "API_BASE_URL=$API_BASE_URL"
fi

echo "Done. Clients now have .env.local with API_BASE_URL=$API_BASE_URL"
