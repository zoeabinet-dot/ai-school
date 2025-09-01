#!/usr/bin/env bash
# Helper to run the local development stack using the development web server (live reload)
# Defaults to the `web-dev` service for iterative development. Pass `--with-nginx` to include nginx.
set -euo pipefail

if [ ! -f .env.compose ]; then
  echo "Create .env.compose from .env.compose.example and set SECRET_KEY before running."
  exit 1
fi

# Default services for iterative development
INCLUDE_NGINX=false
SERVICES=(web-dev db redis)

if [ "${1:-}" = "--with-nginx" ]; then
  INCLUDE_NGINX=true
  SERVICES+=(nginx)
fi

echo "Starting services: ${SERVICES[*]}"

# Use docker compose v2 command if available and pass the .env.compose file
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose --env-file .env.compose up --build "${SERVICES[@]}"
else
  docker compose --env-file .env.compose up --build "${SERVICES[@]}"
fi

# Note: This will block; use Ctrl-C to stop containers. To tear down and remove containers run:
#   docker compose down
