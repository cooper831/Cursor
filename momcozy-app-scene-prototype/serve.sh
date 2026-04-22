#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# 若未传端口：从 8765 起找第一个未被占用的端口（避免 Errno 48 Address already in use）
pick_port() {
  local p
  for p in $(seq 8765 8790); do
    if ! lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1; then
      echo "$p"
      return 0
    fi
  done
  echo ""
  return 1
}

if [[ -n "${1:-}" ]]; then
  PORT="$1"
else
  PORT="$(pick_port || true)"
  if [[ -z "$PORT" ]]; then
    echo "8765–8790 端口均被占用。请关闭其它本地服务或手动指定端口：" >&2
    echo "  $0 8800" >&2
    exit 1
  fi
fi

echo "Serving Momcozy prototype at http://127.0.0.1:${PORT}/index.html"
echo "Press Ctrl+C to stop."
exec python3 -m http.server "$PORT"
