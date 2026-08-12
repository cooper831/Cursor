#!/bin/bash
# Cursor stop hook: auto commit/push publishable docs and redeploy Vercel.
set -euo pipefail

cat >/dev/null

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${ROOT}" ]]; then
  exit 0
fi

cd "${ROOT}"

if [[ ! -f scripts/publish-docs.mjs ]]; then
  exit 0
fi

node scripts/publish-docs.mjs || true
exit 0
