#!/usr/bin/env bash
set -euo pipefail

# Wait for DB if DATABASE_URL points to a host that may not be ready
wait_for_db() {
  local retries=30
  local delay=2
  for i in $(seq 1 $retries); do
    if alembic current >/dev/null 2>&1; then
      return 0
    fi
    echo "[entrypoint] DB not ready yet... ($i/$retries)"
    sleep $delay
  done
  echo "[entrypoint] Proceeding even if DB not confirmed (alembic current failed)"
}

# Run migrations
run_migrations() {
  echo "[entrypoint] Running Alembic migrations..."
  alembic upgrade head || {
    echo "[entrypoint] Alembic upgrade failed; continuing to start app" >&2
  }
}

main() {
  # Ensure PYTHONPATH includes app root
  export PYTHONPATH="/app:${PYTHONPATH:-}"
  wait_for_db || true
  run_migrations || true
  echo "[entrypoint] Starting bot..."
  exec python -m bot.app
}

main "$@"
