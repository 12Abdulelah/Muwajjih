#!/usr/bin/env sh
set -eu

IMAGE="${IMAGE:-muwajjih:latest}"
NAME="muwajjih-smoke"
PORT="${PORT:-18000}"

docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --rm --name "$NAME" -p "$PORT:8000" "$IMAGE" >/dev/null
trap 'docker rm -f "$NAME" >/dev/null 2>&1 || true' EXIT

i=0
until curl -fsS "http://127.0.0.1:$PORT/ready" >/dev/null; do
  i=$((i + 1))
  if [ "$i" -ge 30 ]; then
    docker logs "$NAME"
    exit 1
  fi
  sleep 1
done

curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null
curl -fsS -X POST "http://127.0.0.1:$PORT/v1/predict" -H "Content-Type: application/json" -d '{"complaint":"There is a gas leak near my building"}' | grep '"priority":"urgent"' >/dev/null
echo "smoke_test=passed"
