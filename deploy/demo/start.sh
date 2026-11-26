#!/bin/bash
set -euo pipefail

if [[ ! ${PORT:-7860} =~ ^[0-9]{1,5}$ ]] || (( 10#${PORT:-7860} < 1024 || 10#${PORT:-7860} > 65535 )); then
    echo "PORT must be between 1024 and 65535." >&2
    exit 1
fi
sed "s/__PORT__/$((10#${PORT:-7860}))/" /app/nginx.conf > /tmp/layerwise-nginx.conf

pids=()
stop() {
    if (( ${#pids[@]} )); then
        kill "${pids[@]}" 2>/dev/null || true
        wait "${pids[@]}" 2>/dev/null || true
    fi
}
trap stop EXIT
trap 'exit 0' TERM INT

/app/.venv/bin/uvicorn demo_api:app --host 127.0.0.1 --port 8765 --root-path /api &
pids+=("$!")
HOSTNAME=127.0.0.1 PORT=3765 node /app/web/server.js &
pids+=("$!")
nginx -c /tmp/layerwise-nginx.conf -g 'daemon off;' &
pids+=("$!")

wait -n "${pids[@]}"
